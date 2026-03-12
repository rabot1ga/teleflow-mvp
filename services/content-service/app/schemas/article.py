"""
Article-related schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    """Base article schema."""

    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: List[str] = Field(default_factory=list)
    language: str = "ru"
    author: Optional[str] = None


class ArticleCreate(ArticleBase):
    """Article creation schema."""

    project_id: str
    source_id: Optional[str] = None
    image_url: Optional[str] = None
    original_pub_date: Optional[datetime] = None


class ArticleUpdate(BaseModel):
    """Article update schema."""

    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


class ArticleResponse(BaseModel):
    """Article response schema."""

    id: str
    project_id: str
    source_id: Optional[str]
    title: str
    content: Optional[str]
    summary: Optional[str]
    url: Optional[str]
    image_url: Optional[str]
    image_path: Optional[str]
    category: Optional[str]
    tags: List[str]
    language: str
    author: Optional[str]
    quality_score: float
    priority_score: int
    status: str
    moderated_by: Optional[str]
    moderated_at: Optional[datetime]
    rejection_reason: Optional[str]
    published_at: Optional[datetime]
    original_pub_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleList(BaseModel):
    """Article list response schema."""

    items: List[ArticleResponse]
    total: int
    page: int
    per_page: int
    pages: int
