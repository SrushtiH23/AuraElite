"""
Pydantic schemas for SavedRecommendation.
"""

from datetime import datetime
from typing import List, Any
from pydantic import BaseModel


class SavedRecommendationCreate(BaseModel):
    occasion: str
    budget: float
    location: str
    hair_type: str
    explanation: str
    recommended_hairstyles: List[Any]
    recommended_services: List[Any]
    recommended_salons: List[Any]
    estimated_budget: float


class SavedRecommendationOut(BaseModel):
    id: int
    user_id: int
    occasion: str
    budget: float
    location: str
    hair_type: str
    explanation: str
    recommended_hairstyles: Any
    recommended_services: Any
    recommended_salons: Any
    estimated_budget: float
    created_at: datetime

    class Config:
        from_attributes = True
