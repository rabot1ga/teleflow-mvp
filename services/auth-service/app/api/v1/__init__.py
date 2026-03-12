"""
API routers.
"""

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.projects import router as projects_router
from app.api.v1.internal import router as internal_router

__all__ = [
    "auth_router",
    "users_router",
    "projects_router",
    "internal_router",
]
