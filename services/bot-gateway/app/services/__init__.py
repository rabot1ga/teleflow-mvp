"""
Bot Gateway services.
"""

from app.services.content_client import content_service_client
from app.services.funnel_client import funnel_service_client

__all__ = [
    "content_service_client",
    "funnel_service_client",
]
