"""
Service ORM model.
Each service belongs to a salon (foreign key).
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False, index=True)
    service_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)  # e.g. Hair Care, Skin Care
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    duration_minutes = Column(Integer, default=60)

    # Relationship
    salon = relationship("Salon", backref="services", lazy="joined")

    def __repr__(self) -> str:
        return f"<Service id={self.id} name={self.service_name} salon_id={self.salon_id}>"
