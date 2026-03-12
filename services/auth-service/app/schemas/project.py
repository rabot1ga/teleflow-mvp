"""
Project-related schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    name: str
    slug: str
    is_active: bool
    owner_id: str
    settings: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectMemberBase(BaseModel):
    """Base project member schema."""

    role: str = Field(..., min_length=1, max_length=50)


class ProjectMemberAdd(ProjectMemberBase):
    """Add member to project schema."""

    user_id: str


class ProjectMemberResponse(BaseModel):
    """Project member response schema."""

    id: str
    project_id: str
    user_id: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
