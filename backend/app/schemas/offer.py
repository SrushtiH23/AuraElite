"""
Pydantic schemas for Offer payloads.
"""

from typing import Optional
from pydantic import BaseModel, Field


class OfferBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    discount_percentage: int = Field(..., ge=0, le=100)
    original_price: float = Field(..., ge=0.0)
    offer_price: float = Field(..., ge=0.0)
    category: str = Field(..., max_length=100)
    valid_until: str = Field(..., max_length=100)
    is_active: bool = True


class OfferCreate(OfferBase):
    """Payload sent when creating a new offer."""
    salon_id: Optional[int] = None


class OfferUpdate(BaseModel):
    """Payload for updating existing offers."""
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[int] = None
    original_price: Optional[float] = None
    offer_price: Optional[float] = None
    category: Optional[str] = None
    valid_until: Optional[str] = None
    is_active: Optional[bool] = None


class OfferOut(OfferBase):
    """Serialized offer response schema."""
    id: int
    salon_id: int
    salon_name: Optional[str] = None
    salon_image_url: Optional[str] = None
    salon_rating: Optional[float] = None

    class Config:
        from_attributes = True
