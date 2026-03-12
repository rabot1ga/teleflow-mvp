"""
Broadcasts API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.broadcast import BroadcastCreate, BroadcastList, BroadcastResponse, BroadcastUpdate
from app.services.broadcast_service import BroadcastService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/broadcasts", tags=["Broadcasts"])


def get_broadcast_service(db=Depends(get_async_session)) -> BroadcastService:
    """Get broadcast service instance."""
    return BroadcastService(db)


@router.post(
    "",
    response_model=StandardResponse[BroadcastResponse],
    summary="Create broadcast",
)
async def create_broadcast(
    data: BroadcastCreate,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastResponse]:
    """Create a new broadcast."""
    broadcast = await broadcast_service.create_broadcast(data)

    return StandardResponse(
        data=BroadcastResponse.model_validate(broadcast),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[BroadcastList],
    summary="List broadcasts",
)
async def list_broadcasts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastList]:
    """List broadcasts with pagination."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    broadcasts, total = await broadcast_service.list_broadcasts(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        status=status_filter,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=BroadcastList(
            items=[BroadcastResponse.model_validate(b) for b in broadcasts],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{broadcast_id}",
    response_model=StandardResponse[BroadcastResponse],
    summary="Get broadcast by ID",
)
async def get_broadcast(
    broadcast_id: str,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastResponse]:
    """Get broadcast by ID."""
    broadcast = await broadcast_service.get_by_id(broadcast_id)

    if not broadcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broadcast not found",
        )

    return StandardResponse(
        data=BroadcastResponse.model_validate(broadcast),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{broadcast_id}",
    response_model=StandardResponse[BroadcastResponse],
    summary="Update broadcast",
)
async def update_broadcast(
    broadcast_id: str,
    data: BroadcastUpdate,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastResponse]:
    """Update broadcast."""
    broadcast = await broadcast_service.get_by_id(broadcast_id)

    if not broadcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broadcast not found",
        )

    updated_broadcast = await broadcast_service.update_broadcast(broadcast, data)

    return StandardResponse(
        data=BroadcastResponse.model_validate(updated_broadcast),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{broadcast_id}",
    response_model=StandardResponse[bool],
    summary="Delete broadcast",
)
async def delete_broadcast(
    broadcast_id: str,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete broadcast."""
    broadcast = await broadcast_service.get_by_id(broadcast_id)

    if not broadcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broadcast not found",
        )

    await broadcast_service.delete_broadcast(broadcast)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))


@router.post(
    "/{broadcast_id}/start",
    response_model=StandardResponse[BroadcastResponse],
    summary="Start broadcast",
)
async def start_broadcast(
    broadcast_id: str,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastResponse]:
    """Start broadcast."""
    broadcast = await broadcast_service.get_by_id(broadcast_id)

    if not broadcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broadcast not found",
        )

    if broadcast.status not in ["draft", "scheduled", "paused"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot start broadcast with status: {broadcast.status}",
        )

    started_broadcast = await broadcast_service.start_broadcast(broadcast)

    # Trigger Celery task to execute broadcast
    from app.tasks import execute_broadcast
    execute_broadcast.delay(broadcast_id)

    return StandardResponse(
        data=BroadcastResponse.model_validate(started_broadcast),
        meta=ResponseMeta(request_id=""),
    )


@router.post(
    "/{broadcast_id}/cancel",
    response_model=StandardResponse[BroadcastResponse],
    summary="Cancel broadcast",
)
async def cancel_broadcast(
    broadcast_id: str,
    broadcast_service: BroadcastService = Depends(get_broadcast_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[BroadcastResponse]:
    """Cancel broadcast."""
    broadcast = await broadcast_service.get_by_id(broadcast_id)

    if not broadcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broadcast not found",
        )

    if broadcast.status not in ["running", "scheduled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel broadcast with status: {broadcast.status}",
        )

    cancelled_broadcast = await broadcast_service.cancel_broadcast(broadcast)

    return StandardResponse(
        data=BroadcastResponse.model_validate(cancelled_broadcast),
        meta=ResponseMeta(request_id=""),
    )
