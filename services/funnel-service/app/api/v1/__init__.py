"""
Funnel Service API routers.
"""

from app.api.v1.broadcasts import router as broadcasts_router
from app.api.v1.funnels import router as funnels_router
from app.api.v1.internal import router as internal_router
from app.api.v1.lead_magnets import router as lead_magnets_router

__all__ = [
    "broadcasts_router",
    "funnels_router",
    "internal_router",
    "lead_magnets_router",
]
