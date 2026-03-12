"""
Content Service schemas.
"""

from app.schemas.source import (
    SourceCreate,
    SourceList,
    SourceResponse,
    SourceUpdate,
)
from app.schemas.article import (
    ArticleCreate,
    ArticleList,
    ArticleResponse,
    ArticleUpdate,
)

__all__ = [
    "SourceCreate",
    "SourceList",
    "SourceResponse",
    "SourceUpdate",
    "ArticleCreate",
    "ArticleList",
    "ArticleResponse",
    "ArticleUpdate",
]
