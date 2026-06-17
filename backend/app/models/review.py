"""
Review ORM model.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    user_name = Column(String(255), nullable=False, default="Anonymous Elite")
    rating = Column(Integer, nullable=False)  # 1 to 5 stars
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    salon = relationship("Salon", backref="reviews", lazy="select")
    user = relationship("User", backref="reviews", lazy="select")

    def __repr__(self) -> str:
        return f"<Review id={self.id} salon_id={self.salon_id} rating={self.rating}>"
