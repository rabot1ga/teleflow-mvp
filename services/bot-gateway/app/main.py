"""
FastAPI application factory.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot import get_bot, start_bot, stop_bot
from app.config import settings
from app.handlers import dp as handlers_dp  # Import handlers to register routes
from teleflow_common.api.health import router as health_router
from teleflow_common.middleware import (
    CorrelationIDMiddleware,
    LoggingMiddleware,
    register_exception_handlers,
    setup_structlog,
)

bot_task: Optional[asyncio.Task] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global bot_task
    
    # Startup
    setup_structlog(settings.SERVICE_NAME, settings.LOG_LEVEL)
    
    # Start bot in background if token is configured
    if get_bot():
        bot_task = asyncio.create_task(start_bot())
        yield
        await stop_bot()
        if bot_task:
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
    else:
        yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    # Create application
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Bot Gateway for TeleFlow Platform",
        version=settings.SERVICE_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
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
    from app.api.v1 import internal_router

    app.include_router(health_router)
    app.include_router(internal_router)

    return app


app = create_app()
