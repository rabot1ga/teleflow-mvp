"""
Funnel Service models.
"""

from app.models.funnel import Funnel
from app.models.funnel_step import FunnelStep
from app.models.funnel_user import FunnelUser
from app.models.lead_magnet import LeadMagnet
from app.models.broadcast import Broadcast
from app.models.crm_segment import CRMSegment

__all__ = [
    "Funnel",
    "FunnelStep",
    "FunnelUser",
    "LeadMagnet",
    "Broadcast",
    "CRMSegment",
]
