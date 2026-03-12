"""
Funnel Service schemas.
"""

from app.schemas.funnel import (
    FunnelCreate,
    FunnelResponse,
    FunnelUpdate,
)
from app.schemas.step import (
    FunnelStepCreate,
    FunnelStepResponse,
    FunnelStepUpdate,
)
from app.schemas.user import (
    FunnelUserCreate,
    FunnelUserResponse,
)
from app.schemas.lead_magnet import (
    LeadMagnetCreate,
    LeadMagnetResponse,
    LeadMagnetUpdate,
)

__all__ = [
    "FunnelCreate",
    "FunnelResponse",
    "FunnelUpdate",
    "FunnelStepCreate",
    "FunnelStepResponse",
    "FunnelStepUpdate",
    "FunnelUserCreate",
    "FunnelUserResponse",
    "LeadMagnetCreate",
    "LeadMagnetResponse",
    "LeadMagnetUpdate",
]
