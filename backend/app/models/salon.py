"""
Salon ORM model.
"""

from sqlalchemy import Column, Integer, String, Float, Text

from app.db.session import Base


class Salon(Base):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    area = Column(String(255), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    rating = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    price_range = Column(String(20), default="₹₹₹")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<Salon id={self.id} name={self.name}>"
