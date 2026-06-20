"""
Offer ORM model.
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)
    salon_name = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    discount_percentage = Column(Integer, nullable=False)
    original_price = Column(Float, nullable=False)
    offer_price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    valid_until = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship to Salon
    salon = relationship("Salon", backref="offers")

    @property
    def salon_image_url(self) -> str:
        return self.salon.image_url if self.salon else "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&auto=format&fit=crop&q=80"

    @property
    def salon_rating(self) -> float:
        return self.salon.rating if self.salon else 4.5

    def __repr__(self) -> str:
        return f"<Offer id={self.id} title={self.title} salon_id={self.salon_id}>"
