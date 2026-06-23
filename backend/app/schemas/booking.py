"""
Pydantic schemas for Booking operations.

Covers creation, update (cancel), response serialization,
and available time-slot responses.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.salon import SalonOut, ServiceOut


# ── Request Schemas ──────────────────────────────────────────────


class BookingCreate(BaseModel):
    """Payload sent when creating a new booking."""

    salon_id: int
    service_id: int
    booking_date: date
    time_slot: str = Field(
        ...,
        min_length=1,
        description="Time slot string, e.g. '10:00 AM - 11:00 AM'",
    )
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_phone: str = Field(..., min_length=10, max_length=10)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("booking_date")
    @classmethod
    def booking_date_not_in_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Booking date cannot be in the past.")
        return v

    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v_clean = v.strip()
        if not v_clean.isdigit() or len(v_clean) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return v_clean


class BookingCancel(BaseModel):
    """Payload for cancelling a booking (status → cancelled)."""

    reason: Optional[str] = Field(None, max_length=500)


# ── Response Schemas ─────────────────────────────────────────────


class BookingOut(BaseModel):
    """Full booking response with nested salon and service details."""

    id: int
    user_id: int
    salon_id: int
    service_id: int
    booking_date: date
    time_slot: str
    status: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Nested objects
    salon: Optional[SalonOut] = None
    service: Optional[ServiceOut] = None

    class Config:
        from_attributes = True


class BookingListOut(BaseModel):
    """Paginated list wrapper for bookings."""

    total: int
    bookings: list[BookingOut]


# ── Time Slots ───────────────────────────────────────────────────


class TimeSlotOut(BaseModel):
    """A single time slot with availability flag."""

    slot: str
    available: bool


class AvailableSlotsOut(BaseModel):
    """List of time slots for a salon on a given date."""

    salon_id: int
    date: date
    slots: list[TimeSlotOut]
