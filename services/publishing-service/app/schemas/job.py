"""
PublishJob schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PublishJobBase(BaseModel):
    """Base job schema."""

    article_id: str
    scheduled_at: Optional[datetime] = None


class PublishJobCreate(PublishJobBase):
    """Job creation schema."""

    project_id: str
    target_id: str
    template_id: Optional[str] = None


class PublishJobUpdate(BaseModel):
    """Job update schema."""

    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None


class PublishJobResponse(BaseModel):
    """Job response schema."""

    id: str
    project_id: str
    article_id: str
    target_id: str
    template_id: Optional[str]
    scheduled_at: Optional[datetime]
    status: str
    telegram_message_id: Optional[int]
    published_at: Optional[datetime]
    error: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublishJobList(BaseModel):
    """Job list response schema."""

    items: List[PublishJobResponse]
    total: int
    page: int
    per_page: int
    pages: int
