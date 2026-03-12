"""API v1 routers for Analytics Service."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.schemas.analytics import (
    BroadcastStatsResponse,
    ContentStatsResponse,
    FunnelStatsResponse,
    OverviewResponse,
    PromotionStatsResponse,
)
from app.services.dashboard_service import DashboardService
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard/overview", response_model=StandardResponse[OverviewResponse])
async def get_overview(
    project_id: str = Query(...),
    days: int = Query(default=7, ge=1, le=90),
    session: AsyncSession = Depends(get_async_session),
):
    """Get overview dashboard data."""
    service = DashboardService()
    try:
        data = await service.get_overview(session, project_id, days)
        return StandardResponse[OverviewResponse](
            success=True,
            data=OverviewResponse(**data),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/content", response_model=StandardResponse[ContentStatsResponse])
async def get_content_stats(
    project_id: str = Query(...),
    days: int = Query(default=30, ge=1, le=365),
    session: AsyncSession = Depends(get_async_session),
):
    """Get content statistics."""
    service = DashboardService()
    try:
        data = await service.get_content_stats(session, project_id, days)
        return StandardResponse[ContentStatsResponse](
            success=True,
            data=ContentStatsResponse(**data),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/funnels", response_model=StandardResponse[FunnelStatsResponse])
async def get_funnel_stats(
    project_id: str = Query(...),
    days: int = Query(default=30, ge=1, le=365),
    session: AsyncSession = Depends(get_async_session),
):
    """Get funnel statistics."""
    service = DashboardService()
    try:
        data = await service.get_funnel_stats(session, project_id, days)
        return StandardResponse[FunnelStatsResponse](
            success=True,
            data=FunnelStatsResponse(**data),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/broadcasts", response_model=StandardResponse[BroadcastStatsResponse])
async def get_broadcast_stats(
    project_id: str = Query(...),
    days: int = Query(default=30, ge=1, le=365),
    session: AsyncSession = Depends(get_async_session),
):
    """Get broadcast statistics."""
    service = DashboardService()
    try:
        data = await service.get_broadcast_stats(session, project_id, days)
        return StandardResponse[BroadcastStatsResponse](
            success=True,
            data=BroadcastStatsResponse(**data),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/promotion", response_model=StandardResponse[PromotionStatsResponse])
async def get_promotion_stats(
    project_id: str = Query(...),
    days: int = Query(default=30, ge=1, le=365),
    session: AsyncSession = Depends(get_async_session),
):
    """Get promotion statistics."""
    service = DashboardService()
    try:
        data = await service.get_promotion_stats(session, project_id, days)
        return StandardResponse[PromotionStatsResponse](
            success=True,
            data=PromotionStatsResponse(**data),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
