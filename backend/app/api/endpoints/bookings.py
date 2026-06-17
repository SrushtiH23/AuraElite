"""
Booking API endpoints (authenticated).

Routes:
    POST  /api/bookings                   — Create a new booking
    GET   /api/bookings                   — List current user's bookings
    GET   /api/bookings/{booking_id}      — Get a single booking
    PATCH /api/bookings/{booking_id}/cancel — Cancel a booking
    GET   /api/bookings/available-slots    — Available time slots for salon+date
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.booking import Booking, BookingStatus
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import (
    AvailableSlotsOut,
    BookingCancel,
    BookingCreate,
    BookingListOut,
    BookingOut,
    TimeSlotOut,
)

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

# ── Predefined time slots (salon operating hours) ────────────────

ALL_TIME_SLOTS = [
    "09:00 AM - 10:00 AM",
    "10:00 AM - 11:00 AM",
    "11:00 AM - 12:00 PM",
    "12:00 PM - 01:00 PM",
    "01:00 PM - 02:00 PM",
    "02:00 PM - 03:00 PM",
    "03:00 PM - 04:00 PM",
    "04:00 PM - 05:00 PM",
    "05:00 PM - 06:00 PM",
    "06:00 PM - 07:00 PM",
    "07:00 PM - 08:00 PM",
]


# ── GET /api/bookings/available-slots ────────────────────────────
# NOTE: This route MUST be defined before /{booking_id} to avoid
#       FastAPI interpreting "available-slots" as a booking_id.


@router.get(
    "/available-slots",
    response_model=AvailableSlotsOut,
    summary="Get available time slots",
)
def get_available_slots(
    salon_id: int = Query(..., description="Salon ID"),
    date_str: str = Query(
        ..., alias="date", description="Date in YYYY-MM-DD format"
    ),
    db: Session = Depends(get_db),
):
    """
    Return all predefined time slots for a salon on the given date,
    with each slot marked as available or not.
    """
    # Parse and validate date
    try:
        booking_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD.",
        )

    if booking_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot check slots for past dates.",
        )

    # Verify salon exists
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salon with id {salon_id} not found.",
        )

    # Find already-booked slots (confirmed or pending only)
    booked_slots = (
        db.query(Booking.time_slot)
        .filter(
            Booking.salon_id == salon_id,
            Booking.booking_date == booking_date,
            Booking.status.in_(
                [BookingStatus.CONFIRMED.value, BookingStatus.PENDING.value]
            ),
        )
        .all()
    )
    booked_set = {row[0] for row in booked_slots}

    slots = [
        TimeSlotOut(slot=s, available=(s not in booked_set))
        for s in ALL_TIME_SLOTS
    ]

    return AvailableSlotsOut(
        salon_id=salon_id,
        date=booking_date,
        slots=slots,
    )


# ── POST /api/bookings ──────────────────────────────────────────


@router.post(
    "",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking",
)
def create_booking(
    payload: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new booking for the authenticated user.

    Validates:
    - Salon exists
    - Service exists and belongs to the salon
    - Time slot is from the predefined list
    - Slot is not already booked
    - User has no conflicting booking for the same salon+date+time
    """
    # 1. Validate salon
    salon = db.query(Salon).filter(Salon.id == payload.salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salon not found.",
        )

    # 2. Validate service belongs to salon
    service = (
        db.query(Service)
        .filter(
            Service.id == payload.service_id,
            Service.salon_id == payload.salon_id,
        )
        .first()
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found for the selected salon.",
        )

    # 3. Validate time slot string
    if payload.time_slot not in ALL_TIME_SLOTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid time slot. Choose from: {ALL_TIME_SLOTS}",
        )

    # 4. Check slot availability
    conflict = (
        db.query(Booking)
        .filter(
            Booking.salon_id == payload.salon_id,
            Booking.booking_date == payload.booking_date,
            Booking.time_slot == payload.time_slot,
            Booking.status.in_(
                [BookingStatus.CONFIRMED.value, BookingStatus.PENDING.value]
            ),
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time slot is already booked. Please choose another.",
        )

    # 5. Prevent user double-booking same salon+date+time
    user_conflict = (
        db.query(Booking)
        .filter(
            Booking.user_id == current_user.id,
            Booking.booking_date == payload.booking_date,
            Booking.time_slot == payload.time_slot,
            Booking.status.in_(
                [BookingStatus.CONFIRMED.value, BookingStatus.PENDING.value]
            ),
        )
        .first()
    )
    if user_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a booking at this date and time.",
        )

    # 6. Create booking
    booking = Booking(
        user_id=current_user.id,
        salon_id=payload.salon_id,
        service_id=payload.service_id,
        booking_date=payload.booking_date,
        time_slot=payload.time_slot,
        status=BookingStatus.CONFIRMED.value,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        notes=payload.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


# ── GET /api/bookings ────────────────────────────────────────────


@router.get(
    "",
    response_model=BookingListOut,
    summary="List user's bookings",
)
def list_user_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all bookings for the authenticated user, newest first."""
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return BookingListOut(total=len(bookings), bookings=bookings)


# ── GET /api/bookings/{booking_id} ───────────────────────────────


@router.get(
    "/{booking_id}",
    response_model=BookingOut,
    summary="Get booking detail",
)
def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a single booking. Only the owner can access it."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this booking.",
        )

    return booking


# ── PATCH /api/bookings/{booking_id}/cancel ──────────────────────


@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingOut,
    summary="Cancel a booking",
)
def cancel_booking(
    booking_id: int,
    payload: BookingCancel = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cancel a booking. Only the booking owner can cancel.
    Only confirmed or pending bookings can be cancelled.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this booking.",
        )

    if booking.status == BookingStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This booking is already cancelled.",
        )

    if booking.status == BookingStatus.COMPLETED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel a completed booking.",
        )

    booking.status = BookingStatus.CANCELLED.value
    if payload and payload.reason:
        booking.notes = f"Cancelled: {payload.reason}"

    db.commit()
    db.refresh(booking)

    return booking
