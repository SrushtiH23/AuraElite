"""
Pydantic schemas for Salon and Service.
"""

from typing import Optional

from pydantic import BaseModel


# ── Salon ────────────────────────────────────────────────────────


class SalonBase(BaseModel):
    name: str
    area: str
    address: str
    rating: Optional[float] = 0.0
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_range: Optional[str] = "₹₹₹"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SalonCreate(SalonBase):
    pass


class SalonOut(SalonBase):
    id: int

    class Config:
        from_attributes = True


# ── Service ──────────────────────────────────────────────────────


class ServiceBase(BaseModel):
    salon_id: int
    service_name: str
    category: Optional[str] = None
    description: Optional[str] = None
    price: float
    duration_minutes: Optional[int] = 60


class ServiceCreate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    id: int

    class Config:
        from_attributes = True


# ── Service with nested salon info (for booking display) ─────────


class ServiceWithSalon(ServiceOut):
    salon: Optional[SalonOut] = None
