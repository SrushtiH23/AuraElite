"""
FastAPI router for Salon Reviews & Summarization.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.salon import Salon
from app.models.review import Review
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewOut,
    ReviewSummaryRequest,
    ReviewSummaryResponse
)
from app.services.review import summarize_reviews_service

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])
logger = logging.getLogger(__name__)


# ── POST /api/reviews/summarize ─────────────────────────────────

@router.post(
    "/summarize",
    response_model=ReviewSummaryResponse,
    summary="Summarize a list of custom salon reviews using AI",
)
async def summarize_reviews_endpoint(payload: ReviewSummaryRequest):
    """
    Direct endpoint to summarize a raw list of review text strings.
    Useful for ad-hoc analysis.
    """
    try:
        summary = await summarize_reviews_service(payload.reviews)
        return summary
    except Exception as e:
        logger.error(f"Error summarizing reviews: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate review summary: {str(e)}"
        )


# ── GET /api/reviews/salons/{salon_id} ───────────────────────────

@router.get(
    "/salons/{salon_id}",
    response_model=List[ReviewOut],
    summary="Get all reviews for a specific salon",
)
def get_salon_reviews(salon_id: int, db: Session = Depends(get_db)):
    """Retrieve all reviews for the given salon, ordered by newest first."""
    # Verify salon exists
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with ID {salon_id} not found."
        )

    reviews = (
        db.query(Review)
        .filter(Review.salon_id == salon_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return reviews


# ── POST /api/reviews/salons/{salon_id} ──────────────────────────

@router.post(
    "/salons/{salon_id}",
    response_model=ReviewOut,
    summary="Submit a new review for a salon",
)
def create_salon_review(
    salon_id: int,
    payload: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit a review for a salon.
    Associates the review with the logged-in user and updates the salon's aggregate rating.
    """
    # Verify salon exists
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with ID {salon_id} not found."
        )

    # Use the logged-in user's name if they didn't specify one
    user_name = payload.user_name or current_user.full_name
    if not user_name:
        user_name = "Anonymous Elite"

    db_review = Review(
        salon_id=salon_id,
        user_id=current_user.id,
        user_name=user_name,
        rating=payload.rating,
        comment=payload.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Recalculate and update the salon's aggregate rating
    all_reviews = db.query(Review).filter(Review.salon_id == salon_id).all()
    if all_reviews:
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        salon.rating = round(avg_rating, 1)
        db.commit()

    return db_review


# ── GET /api/reviews/salons/{salon_id}/summary ───────────────────

@router.get(
    "/salons/{salon_id}/summary",
    response_model=ReviewSummaryResponse,
    summary="Get AI review summarization for a specific salon",
)
async def get_salon_reviews_summary(salon_id: int, db: Session = Depends(get_db)):
    """
    Aggregate all text reviews for a salon and pass them to the AI Summarization service.
    If no reviews exist, returns an empty summary.
    """
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with ID {salon_id} not found."
        )

    reviews = db.query(Review).filter(Review.salon_id == salon_id).all()
    comments = [r.comment for r in reviews if r.comment and r.comment.strip()]

    if not comments:
        return ReviewSummaryResponse(
            pros=[],
            cons=[],
            summary=f"No text reviews available to summarize for {salon.name} yet.",
            is_mock=True
        )

    try:
        summary = await summarize_reviews_service(comments)
        return summary
    except Exception as e:
        logger.error(f"Error generating review summary for salon {salon_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate review summary: {str(e)}"
        )
