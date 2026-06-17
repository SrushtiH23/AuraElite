"""
Booking ORM model.
Links a user to a salon + service at a specific date/time.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DateTime,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


class BookingStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    PENDING = "pending"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    booking_date = Column(Date, nullable=False)
    time_slot = Column(String(50), nullable=False)  # e.g. "10:00 AM - 11:00 AM"
    status = Column(
        String(20),
        default=BookingStatus.CONFIRMED.value,
        nullable=False,
    )
    customer_name = Column(String(255), nullable=True)
    customer_phone = Column(String(20), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", backref="bookings", lazy="joined")
    salon = relationship("Salon", backref="bookings", lazy="joined")
    service = relationship("Service", backref="bookings", lazy="joined")

    def __repr__(self) -> str:
        return f"<Booking id={self.id} user={self.user_id} salon={self.salon_id} status={self.status}>"
