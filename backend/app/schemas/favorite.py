"""
Pydantic schemas for FavoriteSalon.
"""

from datetime import datetime
from pydantic import BaseModel


class FavoriteSalonOut(BaseModel):
    id: int
    user_id: int
    salon_id: int
    created_at: datetime

    class Config:
        from_attributes = True
