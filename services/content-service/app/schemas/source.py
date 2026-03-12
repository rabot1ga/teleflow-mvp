"""
Source-related schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class SourceBase(BaseModel):
    """Base source schema."""

    name: str = Field(..., min_length=1, max_length=255)
    source_type: str = Field(..., min_length=1, max_length=50)  # rss, json_api, scraper, webhook, telegram
    url: Optional[str] = None
    fetch_interval_minutes: int = Field(default=30, ge=5, le=1440)
    default_category: Optional[str] = Field(None, max_length=100)
    priority_boost: int = Field(default=0, ge=-10, le=10)
    is_active: bool = True


class SourceCreate(SourceBase):
    """Source creation schema."""

    project_id: str
    config: dict = Field(default_factory=dict)
    default_tags: List[str] = Field(default_factory=list)
    reputation: float = Field(default=0.5, ge=0.0, le=1.0)


class SourceUpdate(BaseModel):
    """Source update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = None
    fetch_interval_minutes: Optional[int] = Field(None, ge=5, le=1440)
    default_category: Optional[str] = None
    priority_boost: Optional[int] = Field(None, ge=-10, le=10)
    is_active: Optional[bool] = None
    config: Optional[dict] = None
    default_tags: Optional[List[str]] = None
    reputation: Optional[float] = Field(None, ge=0.0, le=1.0)


class SourceResponse(BaseModel):
    """Source response schema."""

    id: str
    project_id: str
    name: str
    source_type: str
    url: Optional[str]
    config: dict
    fetch_interval_minutes: int
    default_category: Optional[str]
    default_tags: List[str]
    priority_boost: int
    reputation: float
    is_active: bool
    last_fetch_at: Optional[datetime]
    last_error: Optional[str]
    error_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SourceList(BaseModel):
    """Source list response schema."""

    items: List[SourceResponse]
    total: int
    page: int
    per_page: int
    pages: int
