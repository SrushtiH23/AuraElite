"""
Saved Recommendation ORM model.
"""

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class SavedRecommendation(Base):
    __tablename__ = "saved_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    occasion = Column(String(255), nullable=False)
    budget = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    hair_type = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    recommended_hairstyles = Column(Text, nullable=False)  # JSON string
    recommended_services = Column(Text, nullable=False)    # JSON string
    recommended_salons = Column(Text, nullable=False)      # JSON string
    estimated_budget = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", lazy="select")

    def __repr__(self) -> str:
        return f"<SavedRecommendation id={self.id} user_id={self.user_id} occasion={self.occasion}>"
