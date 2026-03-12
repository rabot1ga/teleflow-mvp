"""
Publishing Service API routers.
"""

from app.api.v1.targets import router as targets_router
from app.api.v1.templates import router as templates_router
from app.api.v1.jobs import router as jobs_router

__all__ = [
    "targets_router",
    "templates_router",
    "jobs_router",
]
