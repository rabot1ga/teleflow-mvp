"""
Middleware module for TeleFlow services.
"""

import uuid
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds X-Request-ID header for request tracing.
    Generates a new ID if not present in request headers.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> None:
        # Get or generate correlation ID
        correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Add to request state for logging
        request.state.correlation_id = correlation_id

        # Call next middleware
        response = await call_next(request)

        # Add correlation ID to response headers
        response.headers["X-Request-ID"] = correlation_id

        return response
