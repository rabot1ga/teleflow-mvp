"""
Funnel schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class FunnelBase(BaseModel):
    """Base funnel schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_type: str = Field(..., min_length=1, max_length=50)
    trigger_value: Optional[str] = None
    is_active: bool = True


class FunnelCreate(FunnelBase):
    """Funnel creation schema."""

    project_id: str


class FunnelUpdate(BaseModel):
    """Funnel update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_value: Optional[str] = None
    is_active: Optional[bool] = None


class FunnelResponse(BaseModel):
    """Funnel response schema."""

    id: str
    project_id: str
    name: str
    description: Optional[str]
    trigger_type: str
    trigger_value: Optional[str]
    is_active: bool
    stats: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FunnelList(BaseModel):
    """Funnel list response schema."""

    items: List[FunnelResponse]
    total: int
    page: int
    per_page: int
    pages: int
