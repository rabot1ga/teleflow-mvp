"""
FastAPI application factory for Promotion Service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import tasks_router
from teleflow_common.api.health import router as health_router
from teleflow_common.middleware import (
    CorrelationIDMiddleware,
    LoggingMiddleware,
    register_exception_handlers,
    setup_structlog,
)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    # Setup structured logging
    setup_structlog(settings.SERVICE_NAME, settings.LOG_LEVEL)

    # Create application
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Promotion Service for TeleFlow Platform - Parsing, inviting, masslooking, commenting",
        version=settings.SERVICE_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Add middleware
    app.add_middleware(CorrelationIDMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(health_router)
    app.include_router(tasks_router, prefix="/api/v1/promotion")

    return app


app = create_app()
