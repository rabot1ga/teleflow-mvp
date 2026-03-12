"""
Global error handler middleware.
"""

import json
from datetime import datetime
from typing import Callable

import structlog
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from teleflow_common.schemas.responses import ErrorResponse, ResponseMeta

logger = structlog.get_logger()


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for global error handling.
    Catches all exceptions and returns standardized error responses.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> None:
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self._handle_exception(request, exc, correlation_id)

    async def _handle_exception(
        self, request: Request, exc: Exception, correlation_id: str
    ) -> JSONResponse:
        """Handle exception and return error response."""

        # Log the exception
        logger.error(
            "unhandled_exception",
            path=request.url.path,
            method=request.method,
            exception_type=type(exc).__name__,
            correlation_id=correlation_id,
            exc_info=exc,
        )

        # Handle different exception types
        if isinstance(exc, HTTPException) or isinstance(exc, StarletteHTTPException):
            return self._http_error_response(exc, correlation_id)
        elif isinstance(exc, RequestValidationError):
            return self._validation_error_response(exc, correlation_id)
        else:
            return self._internal_error_response(correlation_id)

    def _http_error_response(
        self, exc: HTTPException, correlation_id: str
    ) -> JSONResponse:
        """Handle HTTP exceptions."""
        error_response = ErrorResponse.create(
            code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    def _validation_error_response(
        self, exc: RequestValidationError, correlation_id: str
    ) -> JSONResponse:
        """Handle validation errors."""
        errors = []
        for error in exc.errors():
            errors.append(
                {
                    "field": ".".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "code": error.get("type"),
                }
            )

        error_response = ErrorResponse.create(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=[type("ErrorDetail", (), d) for d in errors],
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=422,
            content=error_response.model_dump(),
        )

    def _internal_error_response(self, correlation_id: str) -> JSONResponse:
        """Handle internal server errors."""
        error_response = ErrorResponse.create(
            code="INTERNAL_ERROR",
            message="An internal error occurred. Please try again later.",
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(),
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers on FastAPI app.
    Alternative to using middleware.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger.error(
            "http_exception",
            path=request.url.path,
            status_code=exc.status_code,
            detail=exc.detail,
            correlation_id=correlation_id,
        )
        error_response = ErrorResponse.create(
            code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=json.dumps(error_response.model_dump(), cls=DateTimeEncoder),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger.warning(
            "validation_error",
            path=request.url.path,
            errors=exc.errors(),
            correlation_id=correlation_id,
        )
        errors = [
            {
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "code": error.get("type"),
            }
            for error in exc.errors()
        ]
        error_response = ErrorResponse.create(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=errors,
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=422,
            content=json.dumps(error_response.model_dump(), cls=DateTimeEncoder),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger.error(
            "unhandled_exception",
            path=request.url.path,
            exception_type=type(exc).__name__,
            correlation_id=correlation_id,
            exc_info=exc,
        )
        error_response = ErrorResponse.create(
            code="INTERNAL_ERROR",
            message="An internal error occurred. Please try again later.",
            request_id=correlation_id,
        )
        return JSONResponse(
            status_code=500,
            content=json.dumps(error_response.model_dump(), cls=DateTimeEncoder),
        )
