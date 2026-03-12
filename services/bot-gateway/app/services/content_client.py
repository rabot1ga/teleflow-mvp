"""
Content Service client for Bot Gateway.
"""

from typing import Optional

import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


class ContentServiceClient:
    """Client for Content Service API."""

    def __init__(self):
        self.base_url = settings.CONTENT_SERVICE_URL
        self.timeout = 30.0

    async def get_moderation_queue(
        self,
        page: int = 1,
        per_page: int = 5,
        status: str = "pending",
    ) -> Optional[dict]:
        """Get moderation queue."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/content/moderation/queue",
                    params={"page": page, "per_page": per_page, "status": status},
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}) if data.get("success") else None
        except Exception as e:
            logger.error("content_service_error", operation="get_moderation_queue", error=str(e))
            return None

    async def approve_article(self, article_id: str, target_id: Optional[str] = None) -> bool:
        """Approve article."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {"target_id": target_id} if target_id else {}
                response = await client.post(
                    f"{self.base_url}/api/v1/content/articles/{article_id}/approve",
                    params=params,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("success", False)
        except Exception as e:
            logger.error("content_service_error", operation="approve_article", error=str(e))
            return False

    async def reject_article(
        self,
        article_id: str,
        reason: str,
        comment: Optional[str] = None,
    ) -> bool:
        """Reject article."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {"reason": reason}
                if comment:
                    params["comment"] = comment
                response = await client.post(
                    f"{self.base_url}/api/v1/content/articles/{article_id}/reject",
                    params=params,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("success", False)
        except Exception as e:
            logger.error("content_service_error", operation="reject_article", error=str(e))
            return False

    async def get_stats(self) -> Optional[dict]:
        """Get moderation stats."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/content/moderation/stats",
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}) if data.get("success") else None
        except Exception as e:
            logger.error("content_service_error", operation="get_stats", error=str(e))
            return None


# Global client instance
content_service_client = ContentServiceClient()
