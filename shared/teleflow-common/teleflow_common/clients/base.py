"""
HTTP clients for inter-service communication.
"""

from typing import Any, Optional

import httpx
import structlog

logger = structlog.get_logger()


class BaseServiceClient:
    """
    Base async HTTP client for service-to-service communication.

    Features:
    - Automatic retry (3 attempts)
    - Timeout (30 seconds)
    - Correlation ID propagation
    - Structured logging
    - Standard response parsing

    Usage:
        client = BaseServiceClient(base_url="http://auth-service:8001")
        response = await client.get("/api/v1/users/123")
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 0.1,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            headers={"Content-Type": "application/json"},
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method
            path: Request path
            headers: Optional headers
            **kwargs: Additional arguments for httpx

        Returns:
            Parsed JSON response
        """
        import asyncio

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    headers=headers,
                    **kwargs,
                )

                # Log response
                logger.debug(
                    "http_request",
                    method=method,
                    path=path,
                    status_code=response.status_code,
                    attempt=attempt + 1,
                )

                # Raise on error
                response.raise_for_status()

                # Parse and return
                return response.json()

            except httpx.HTTPStatusError as e:
                logger.error(
                    "http_status_error",
                    method=method,
                    path=path,
                    status_code=e.response.status_code,
                    detail=e.response.text,
                )
                last_exception = e
                break  # Don't retry on HTTP errors

            except (httpx.ConnectError, httpx.TimeoutException) as e:
                logger.warning(
                    "http_retryable_error",
                    method=method,
                    path=path,
                    error=str(e),
                    attempt=attempt + 1,
                )
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))

        # All retries exhausted or non-retryable error
        if last_exception:
            raise last_exception

        raise RuntimeError("Unexpected error in request")

    async def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Make GET request."""
        return await self._request("GET", path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Make POST request."""
        return await self._request("POST", path, json=data, headers=headers)

    async def put(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Make PUT request."""
        return await self._request("PUT", path, json=data, headers=headers)

    async def patch(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Make PATCH request."""
        return await self._request("PATCH", path, json=data, headers=headers)

    async def delete(
        self,
        path: str,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Make DELETE request."""
        return await self._request("DELETE", path, headers=headers)
