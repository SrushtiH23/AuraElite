"""
Favorite Salon ORM model.
"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class FavoriteSalon(Base):
    __tablename__ = "favorite_salons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    salon = relationship("Salon", lazy="joined")
    user = relationship("User", lazy="select")

    __table_args__ = (
        UniqueConstraint("user_id", "salon_id", name="uq_user_salon_favorite"),
    )

    def __repr__(self) -> str:
        return f"<FavoriteSalon id={self.id} user_id={self.user_id} salon_id={self.salon_id}>"
