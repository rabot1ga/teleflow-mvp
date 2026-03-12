"""
PublishTarget schemas.
"""

from datetime import datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field


class PublishTargetBase(BaseModel):
    """Base target schema."""

    name: str = Field(..., min_length=1, max_length=255)
    telegram_chat_id: int
    is_default: bool = False
    min_interval_seconds: int = Field(default=300, ge=60)
    max_per_hour: int = Field(default=6, ge=1)
    max_per_day: int = Field(default=30, ge=1)
    timezone: str = "Europe/Moscow"
    categories: List[str] = Field(default_factory=list)
    is_active: bool = True


class PublishTargetCreate(PublishTargetBase):
    """Target creation schema."""

    project_id: str


class PublishTargetUpdate(BaseModel):
    """Target update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    telegram_chat_title: Optional[str] = None
    is_default: Optional[bool] = None
    min_interval_seconds: Optional[int] = Field(None, ge=60)
    max_per_hour: Optional[int] = Field(None, ge=1)
    max_per_day: Optional[int] = Field(None, ge=1)
    timezone: Optional[str] = None
    categories: Optional[List[str]] = None
    is_active: Optional[bool] = None


class PublishTargetResponse(BaseModel):
    """Target response schema."""

    id: str
    project_id: str
    name: str
    telegram_chat_id: int
    telegram_chat_title: Optional[str]
    is_default: bool
    is_verified: bool
    min_interval_seconds: int
    max_per_hour: int
    max_per_day: int
    working_hours_start: Optional[time]
    working_hours_end: Optional[time]
    timezone: str
    categories: List[str]
    default_template_id: Optional[str]
    is_active: bool
    last_published_at: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublishTargetList(BaseModel):
    """Target list response schema."""

    items: List[PublishTargetResponse]
    total: int
    page: int
    per_page: int
    pages: int
