"""
FastAPI application factory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.dependencies import get_async_session
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
        description="Auth Service for TeleFlow Platform",
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
        allow_origins=["*"],  # Configure in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    from app.api.v1 import auth_router, users_router, projects_router, internal_router

    app.include_router(health_router)
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(projects_router, prefix="/api/v1")
    app.include_router(internal_router)  # Internal endpoints don't have /api/v1 prefix

    return app


app = create_app()
