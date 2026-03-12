"""
User-related schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """User update schema."""

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    telegram_username: Optional[str] = Field(None, max_length=100)


class UserResponse(BaseModel):
    """User response schema."""

    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    is_active: bool
    is_email_verified: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
