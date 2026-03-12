"""
Health check endpoints for TeleFlow services.
"""

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime


class ReadyResponse(BaseModel):
    """Readiness check response."""

    status: str
    version: str
    timestamp: datetime
    dependencies: dict[str, bool]


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(version: str = "0.1.0") -> HealthResponse:
    """
    Basic health check endpoint.
    Returns 200 OK if service is running.
    """
    return HealthResponse(
        status="healthy",
        version=version,
        timestamp=datetime.utcnow(),
    )


@router.get("/health/ready", response_model=ReadyResponse, tags=["Health"])
async def readiness_check(
    version: str = "0.1.0",
    db_check: bool = True,
    redis_check: bool = True,
) -> ReadyResponse:
    """
    Readiness check endpoint.
    Returns 200 OK if service is ready to handle requests.
    """
    dependencies = {
        "database": db_check,
        "redis": redis_check,
    }

    all_healthy = all(dependencies.values())

    return ReadyResponse(
        status="ready" if all_healthy else "not_ready",
        version=version,
        timestamp=datetime.utcnow(),
        dependencies=dependencies,
    )
