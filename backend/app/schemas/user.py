"""
Pydantic schemas for User and Token payloads.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ── User Schemas ─────────────────────────────────────────────────


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    salon_id: Optional[int] = None


class UserCreate(UserBase):
    """Payload sent when a new user registers."""

    password: str = Field(..., min_length=6, description="Minimum 6 characters")


class UserUpdate(BaseModel):
    """Payload for updating user profile fields."""

    full_name: Optional[str] = None
    password: Optional[str] = Field(
        None, min_length=6, description="Leave blank to keep current"
    )


class UserOut(UserBase):
    """Serialized user returned by the API (never exposes password)."""

    id: int
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Token Schemas ────────────────────────────────────────────────


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
