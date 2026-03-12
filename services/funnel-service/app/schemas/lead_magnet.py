"""
LeadMagnet schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class LeadMagnetBase(BaseModel):
    """Base lead magnet schema."""

    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    delivery_message: str
    require_subscription: bool = True


class LeadMagnetCreate(LeadMagnetBase):
    """Lead magnet creation schema."""

    project_id: str
    file_id: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    text_content: Optional[str] = None
    subscription_channel_id: Optional[int] = None


class LeadMagnetUpdate(BaseModel):
    """Lead magnet update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = None
    description: Optional[str] = None
    delivery_message: Optional[str] = None
    require_subscription: Optional[bool] = None


class LeadMagnetResponse(BaseModel):
    """Lead magnet response schema."""

    id: str
    project_id: str
    name: str
    type: str
    description: Optional[str]
    file_id: Optional[str]
    file_path: Optional[str]
    url: Optional[str]
    text_content: Optional[str]
    delivery_message: str
    require_subscription: bool
    subscription_channel_id: Optional[int]
    stats: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadMagnetList(BaseModel):
    """Lead magnet list response schema."""

    items: List[LeadMagnetResponse]
    total: int
    page: int
    per_page: int
    pages: int
