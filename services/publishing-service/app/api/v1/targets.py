"""
Publish Targets API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.target import PublishTargetCreate, PublishTargetList, PublishTargetResponse, PublishTargetUpdate
from app.services.target_service import PublishTargetService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/targets", tags=["Publish Targets"])


def get_target_service(db=Depends(get_async_session)) -> PublishTargetService:
    """Get target service instance."""
    return PublishTargetService(db)


@router.post(
    "",
    response_model=StandardResponse[PublishTargetResponse],
    summary="Create publish target",
)
async def create_target(
    data: PublishTargetCreate,
    target_service: PublishTargetService = Depends(get_target_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTargetResponse]:
    """Create a new publish target (Telegram channel)."""
    target = await target_service.create_target(data)

    return StandardResponse(
        data=PublishTargetResponse.model_validate(target),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[PublishTargetList],
    summary="List publish targets",
)
async def list_targets(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = None,
    target_service: PublishTargetService = Depends(get_target_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTargetList]:
    """List publish targets with pagination."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    targets, total = await target_service.list_targets(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        is_active=is_active,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=PublishTargetList(
            items=[PublishTargetResponse.model_validate(t) for t in targets],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{target_id}",
    response_model=StandardResponse[PublishTargetResponse],
    summary="Get publish target by ID",
)
async def get_target(
    target_id: str,
    target_service: PublishTargetService = Depends(get_target_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTargetResponse]:
    """Get publish target by ID."""
    target = await target_service.get_by_id(target_id)

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        )

    return StandardResponse(
        data=PublishTargetResponse.model_validate(target),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{target_id}",
    response_model=StandardResponse[PublishTargetResponse],
    summary="Update publish target",
)
async def update_target(
    target_id: str,
    data: PublishTargetUpdate,
    target_service: PublishTargetService = Depends(get_target_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTargetResponse]:
    """Update publish target."""
    target = await target_service.get_by_id(target_id)

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        )

    updated_target = await target_service.update_target(target, data)

    return StandardResponse(
        data=PublishTargetResponse.model_validate(updated_target),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{target_id}",
    response_model=StandardResponse[bool],
    summary="Delete publish target",
)
async def delete_target(
    target_id: str,
    target_service: PublishTargetService = Depends(get_target_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete publish target."""
    target = await target_service.get_by_id(target_id)

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        )

    await target_service.delete_target(target)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
