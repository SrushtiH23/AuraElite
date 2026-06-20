"""
Offers API endpoints.

Routes:
    GET  /offers/active           — List all active offers (unauthenticated)
    GET  /api/offers/active       — Alias for active offers
    GET  /api/offers/my           — List owner's salon offers (authenticated)
    POST /api/offers              — Create a new offer (authenticated)
    PUT  /api/offers/{offer_id}   — Edit an offer (authenticated)
    POST /api/offers/{offer_id}/expire — Expire an offer (authenticated)
    DELETE /api/offers/{offer_id} — Delete an offer (authenticated)
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.offer import Offer
from app.models.salon import Salon
from app.models.user import User
from app.schemas.offer import OfferCreate, OfferOut, OfferUpdate

# We declare the router with prefix /api/offers, but we will also add a duplicate router or path decorators for /offers/active
router = APIRouter(prefix="/api/offers", tags=["Offers"])


# ── GET active offers (Unauthenticated) ──────────────────────────

@router.get(
    "/active",
    response_model=List[OfferOut],
    summary="Get all active offers (prefixed)",
)
def get_active_offers_prefixed(db: Session = Depends(get_db)):
    """Return all active offers where is_active is True, sorted by valid_until."""
    return db.query(Offer).filter(Offer.is_active == True).all()


# We create a separate router for the un-prefixed '/offers' routes to support both requirements
unprefixed_router = APIRouter(prefix="/offers", tags=["Offers Unprefixed"])

@unprefixed_router.get(
    "/active",
    response_model=List[OfferOut],
    summary="Get all active offers (unprefixed)",
)
def get_active_offers_unprefixed(db: Session = Depends(get_db)):
    """Return all active offers where is_active is True, sorted by valid_until."""
    return db.query(Offer).filter(Offer.is_active == True).all()


# ── GET owner's salon offers (Authenticated) ────────────────────

@router.get(
    "/my",
    response_model=List[OfferOut],
    summary="Get current salon owner's offers",
)
def get_my_salon_offers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all offers belonging to the authenticated salon owner's salon."""
    if not current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only registered salon owners can view their salon's offers.",
        )
    return db.query(Offer).filter(Offer.salon_id == current_user.salon_id).all()


# ── POST create offer (Authenticated) ───────────────────────────

@router.post(
    "",
    response_model=OfferOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new salon offer",
)
def create_offer(
    payload: OfferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new offer for the salon owned by the current user."""
    if not current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only registered salon owners can create offers.",
        )

    salon = db.query(Salon).filter(Salon.id == current_user.salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated salon not found.",
        )

    offer = Offer(
        salon_id=salon.id,
        salon_name=salon.name,
        title=payload.title,
        description=payload.description,
        discount_percentage=payload.discount_percentage,
        original_price=payload.original_price,
        offer_price=payload.offer_price,
        category=payload.category,
        valid_until=payload.valid_until,
        is_active=payload.is_active,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    return offer


# ── PUT update offer (Authenticated) ────────────────────────────

@router.put(
    "/{offer_id}",
    response_model=OfferOut,
    summary="Edit an existing offer",
)
def update_offer(
    offer_id: int,
    payload: OfferUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Edit an existing offer. The owner's salon must match the offer's salon."""
    if not current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only registered salon owners can update offers.",
        )

    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with id {offer_id} not found.",
        )

    if offer.salon_id != current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this offer.",
        )

    # Apply updates
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(offer, field, value)

    db.commit()
    db.refresh(offer)

    return offer


# ── POST expire offer (Authenticated) ───────────────────────────

@router.post(
    "/{offer_id}/expire",
    response_model=OfferOut,
    summary="Expire an offer",
)
def expire_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Expire an existing offer (set is_active = False)."""
    if not current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only registered salon owners can expire offers.",
        )

    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with id {offer_id} not found.",
        )

    if offer.salon_id != current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to expire this offer.",
        )

    offer.is_active = False
    db.commit()
    db.refresh(offer)

    return offer


# ── DELETE delete offer (Authenticated) ────────────────────────

@router.delete(
    "/{offer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an offer",
)
def delete_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an existing offer."""
    if not current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only registered salon owners can delete offers.",
        )

    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with id {offer_id} not found.",
        )

    if offer.salon_id != current_user.salon_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this offer.",
        )

    db.delete(offer)
    db.commit()

    return None
