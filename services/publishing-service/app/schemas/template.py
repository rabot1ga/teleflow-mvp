"""
PublishTemplate schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PublishTemplateBase(BaseModel):
    """Base template schema."""

    name: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)
    parse_mode: str = "HTML"
    disable_preview: bool = False
    buttons: List[dict] = Field(default_factory=list)
    scope: str = "global"
    is_active: bool = True


class PublishTemplateCreate(PublishTemplateBase):
    """Template creation schema."""

    project_id: str
    description: Optional[str] = None
    scope_value: Optional[str] = None


class PublishTemplateUpdate(BaseModel):
    """Template update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    body: Optional[str] = Field(None, min_length=1)
    parse_mode: Optional[str] = None
    disable_preview: Optional[bool] = None
    buttons: Optional[List[dict]] = None
    scope: Optional[str] = None
    is_active: Optional[bool] = None


class PublishTemplateResponse(BaseModel):
    """Template response schema."""

    id: str
    project_id: str
    name: str
    description: Optional[str]
    body: str
    parse_mode: str
    disable_preview: bool
    buttons: List[dict]
    scope: str
    scope_value: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublishTemplateList(BaseModel):
    """Template list response schema."""

    items: List[PublishTemplateResponse]
    total: int
    page: int
    per_page: int
    pages: int
