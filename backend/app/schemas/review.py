"""
Pydantic schemas for Review and ReviewSummary.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ── Review Schemas ──────────────────────────────────────────────

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: str = Field(..., description="Review comment")
    user_name: Optional[str] = Field("Anonymous Elite", description="Reviewer name")


class ReviewCreate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int
    salon_id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Review Summarization Schemas ─────────────────────────────────

class ReviewSummaryRequest(BaseModel):
    reviews: List[str] = Field(..., description="List of reviews to summarize")


class ReviewSummaryResponse(BaseModel):
    pros: List[str] = Field(..., description="Positive aspects identified in the reviews")
    cons: List[str] = Field(..., description="Negative aspects or areas of improvement identified in the reviews")
    summary: str = Field(..., description="A synthesized summary of all reviews")
    is_mock: bool = Field(False, description="Indicates if the summary was generated using the fallback mock logic")
