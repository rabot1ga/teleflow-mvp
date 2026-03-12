"""
Broadcast schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BroadcastBase(BaseModel):
    """Base broadcast schema."""

    name: str = Field(..., min_length=1, max_length=255)
    message_type: str = "text"
    message_text: str
    message_media_url: Optional[str] = None
    buttons: Optional[dict] = None
    recipient_filter: dict = Field(default_factory=lambda: {"type": "all"})
    send_rate: int = Field(default=30, ge=1, le=100)


class BroadcastCreate(BroadcastBase):
    """Broadcast creation schema."""

    project_id: str
    scheduled_at: Optional[datetime] = None


class BroadcastUpdate(BaseModel):
    """Broadcast update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    message_text: Optional[str] = None
    message_media_url: Optional[str] = None
    buttons: Optional[dict] = None
    recipient_filter: Optional[dict] = None
    send_rate: Optional[int] = Field(None, ge=1, le=100)
    scheduled_at: Optional[datetime] = None


class BroadcastResponse(BaseModel):
    """Broadcast response schema."""

    id: str
    project_id: str
    name: str
    message_type: str
    message_text: str
    message_media_url: Optional[str]
    buttons: Optional[dict]
    recipient_filter: dict
    scheduled_at: Optional[datetime]
    status: str
    total_recipients: int
    sent: int
    delivered: int
    failed: int
    send_rate: int
    created_by: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BroadcastList(BaseModel):
    """Broadcast list response schema."""

    items: List[BroadcastResponse]
    total: int
    page: int
    per_page: int
    pages: int
