"""
Content Service API routers.
"""

from app.api.v1.sources import router as sources_router
from app.api.v1.articles import router as articles_router
from app.api.v1.moderation import router as moderation_router
from app.api.v1.ai import router as ai_router

__all__ = [
    "sources_router",
    "articles_router",
    "moderation_router",
    "ai_router",
]
