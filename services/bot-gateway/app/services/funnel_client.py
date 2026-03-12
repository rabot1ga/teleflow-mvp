"""
Funnel Service client for Bot Gateway.
"""

from typing import Optional

import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


class FunnelServiceClient:
    """Client for Funnel Service API."""

    def __init__(self):
        self.base_url = settings.FUNNEL_SERVICE_URL
        self.timeout = 30.0

    async def trigger_funnel(
        self,
        telegram_user_id: int,
        trigger_type: str,
        trigger_value: str,
    ) -> Optional[dict]:
        """Trigger funnel for a user."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/funnels/trigger",
                    json={
                        "telegram_user_id": telegram_user_id,
                        "trigger_type": trigger_type,
                        "trigger_value": trigger_value,
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}) if data.get("success") else None
        except Exception as e:
            logger.error("funnel_service_error", operation="trigger_funnel", error=str(e))
            return None

    async def get_user_status(
        self,
        telegram_user_id: int,
        funnel_id: str,
    ) -> Optional[dict]:
        """Get user status in funnel."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/funnels/{funnel_id}/users/{telegram_user_id}"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}) if data.get("success") else None
        except Exception as e:
            logger.error("funnel_service_error", operation="get_user_status", error=str(e))
            return None

    async def get_lead_magnet(self, magnet_id: str) -> Optional[dict]:
        """Get lead magnet by ID."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/funnels/lead-magnets/{magnet_id}"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}) if data.get("success") else None
        except Exception as e:
            logger.error("funnel_service_error", operation="get_lead_magnet", error=str(e))
            return None


# Global client instance
funnel_service_client = FunnelServiceClient()
