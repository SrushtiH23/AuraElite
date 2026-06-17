"""
Salon & Service listing API endpoints (public).

Routes:
    GET /api/salons              — List all salons
    GET /api/salons/{salon_id}   — Get a single salon by ID
    GET /api/salons/{salon_id}/services — List services for a salon
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User
from app.models.favorite import FavoriteSalon
from app.schemas.salon import SalonOut, ServiceOut

router = APIRouter(prefix="/api/salons", tags=["Salons"])


# ── GET /api/salons ──────────────────────────────────────────────


@router.get(
    "",
    response_model=list[SalonOut],
    summary="List all salons",
)
def list_salons(db: Session = Depends(get_db)):
    """Return every salon in the database."""
    salons = db.query(Salon).order_by(Salon.name).all()
    return salons


# ── GET /api/salons/favorites ───────────────────────────────────


@router.get(
    "/favorites",
    response_model=list[SalonOut],
    summary="Get user's favorite salons",
)
def get_favorite_salons(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all salons favorited by the authenticated user."""
    favorites = (
        db.query(Salon)
        .join(FavoriteSalon, FavoriteSalon.salon_id == Salon.id)
        .filter(FavoriteSalon.user_id == current_user.id)
        .order_by(Salon.name)
        .all()
    )
    return favorites


# ── POST /api/salons/{salon_id}/favorite ─────────────────────────


@router.post(
    "/{salon_id}/favorite",
    summary="Toggle salon favorite status",
)
def toggle_favorite_salon(
    salon_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Toggle favorite status of a salon. Returns whether it is now favorited."""
    # Verify salon exists
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with ID {salon_id} not found."
        )

    # Check if already favorited
    fav = (
        db.query(FavoriteSalon)
        .filter(
            FavoriteSalon.user_id == current_user.id,
            FavoriteSalon.salon_id == salon_id
        )
        .first()
    )

    if fav:
        db.delete(fav)
        db.commit()
        return {"salon_id": salon_id, "is_favorite": False}
    else:
        new_fav = FavoriteSalon(user_id=current_user.id, salon_id=salon_id)
        db.add(new_fav)
        db.commit()
        return {"salon_id": salon_id, "is_favorite": True}


# ── GET /api/salons/{salon_id} ───────────────────────────────────


@router.get(
    "/{salon_id}",
    response_model=SalonOut,
    summary="Get salon by ID",
)
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    """Return a single salon or 404."""
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with id {salon_id} not found.",
        )
    return salon


# ── GET /api/salons/{salon_id}/services ──────────────────────────


@router.get(
    "/{salon_id}/services",
    response_model=list[ServiceOut],
    summary="List services for a salon",
)
def list_salon_services(salon_id: int, db: Session = Depends(get_db)):
    """Return all services belonging to the given salon."""
    # Verify salon exists
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with id {salon_id} not found.",
        )

    services = (
        db.query(Service)
        .filter(Service.salon_id == salon_id)
        .order_by(Service.category, Service.service_name)
        .all()
    )
    return services
