"""
Funnels API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.funnel import FunnelCreate, FunnelList, FunnelResponse, FunnelUpdate
from app.services.funnel_service import FunnelService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/funnels", tags=["Funnels"])


def get_funnel_service(db=Depends(get_async_session)) -> FunnelService:
    """Get funnel service instance."""
    return FunnelService(db)


@router.post(
    "",
    response_model=StandardResponse[FunnelResponse],
    summary="Create funnel",
)
async def create_funnel(
    data: FunnelCreate,
    funnel_service: FunnelService = Depends(get_funnel_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[FunnelResponse]:
    """Create a new funnel."""
    funnel = await funnel_service.create_funnel(data)

    return StandardResponse(
        data=FunnelResponse.model_validate(funnel),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[FunnelList],
    summary="List funnels",
)
async def list_funnels(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = None,
    funnel_service: FunnelService = Depends(get_funnel_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[FunnelList]:
    """List funnels with pagination."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    funnels, total = await funnel_service.list_funnels(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        is_active=is_active,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=FunnelList(
            items=[FunnelResponse.model_validate(f) for f in funnels],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{funnel_id}",
    response_model=StandardResponse[FunnelResponse],
    summary="Get funnel by ID",
)
async def get_funnel(
    funnel_id: str,
    funnel_service: FunnelService = Depends(get_funnel_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[FunnelResponse]:
    """Get funnel by ID."""
    funnel = await funnel_service.get_by_id(funnel_id)

    if not funnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funnel not found",
        )

    return StandardResponse(
        data=FunnelResponse.model_validate(funnel),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{funnel_id}",
    response_model=StandardResponse[FunnelResponse],
    summary="Update funnel",
)
async def update_funnel(
    funnel_id: str,
    data: FunnelUpdate,
    funnel_service: FunnelService = Depends(get_funnel_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[FunnelResponse]:
    """Update funnel."""
    funnel = await funnel_service.get_by_id(funnel_id)

    if not funnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funnel not found",
        )

    updated_funnel = await funnel_service.update_funnel(funnel, data)

    return StandardResponse(
        data=FunnelResponse.model_validate(updated_funnel),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{funnel_id}",
    response_model=StandardResponse[bool],
    summary="Delete funnel",
)
async def delete_funnel(
    funnel_id: str,
    funnel_service: FunnelService = Depends(get_funnel_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete funnel."""
    funnel = await funnel_service.get_by_id(funnel_id)

    if not funnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funnel not found",
        )

    await funnel_service.delete_funnel(funnel)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
