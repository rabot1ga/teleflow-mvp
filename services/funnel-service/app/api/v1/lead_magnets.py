"""
Lead Magnets API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.lead_magnet import LeadMagnetCreate, LeadMagnetList, LeadMagnetResponse, LeadMagnetUpdate
from app.services.lead_magnet_service import LeadMagnetService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/lead-magnets", tags=["Lead Magnets"])


def get_lead_magnet_service(db=Depends(get_async_session)) -> LeadMagnetService:
    """Get lead magnet service instance."""
    return LeadMagnetService(db)


@router.post(
    "",
    response_model=StandardResponse[LeadMagnetResponse],
    summary="Create lead magnet",
)
async def create_lead_magnet(
    data: LeadMagnetCreate,
    magnet_service: LeadMagnetService = Depends(get_lead_magnet_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[LeadMagnetResponse]:
    """Create a new lead magnet."""
    magnet = await magnet_service.create_lead_magnet(data)

    return StandardResponse(
        data=LeadMagnetResponse.model_validate(magnet),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[LeadMagnetList],
    summary="List lead magnets",
)
async def list_lead_magnets(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    magnet_service: LeadMagnetService = Depends(get_lead_magnet_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[LeadMagnetList]:
    """List lead magnets with pagination."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    magnets, total = await magnet_service.list_lead_magnets(
        project_id=project_id,
        skip=skip,
        limit=per_page,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=LeadMagnetList(
            items=[LeadMagnetResponse.model_validate(m) for m in magnets],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{magnet_id}",
    response_model=StandardResponse[LeadMagnetResponse],
    summary="Get lead magnet by ID",
)
async def get_lead_magnet(
    magnet_id: str,
    magnet_service: LeadMagnetService = Depends(get_lead_magnet_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[LeadMagnetResponse]:
    """Get lead magnet by ID."""
    magnet = await magnet_service.get_by_id(magnet_id)

    if not magnet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead magnet not found",
        )

    return StandardResponse(
        data=LeadMagnetResponse.model_validate(magnet),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{magnet_id}",
    response_model=StandardResponse[LeadMagnetResponse],
    summary="Update lead magnet",
)
async def update_lead_magnet(
    magnet_id: str,
    data: LeadMagnetUpdate,
    magnet_service: LeadMagnetService = Depends(get_lead_magnet_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[LeadMagnetResponse]:
    """Update lead magnet."""
    magnet = await magnet_service.get_by_id(magnet_id)

    if not magnet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead magnet not found",
        )

    updated_magnet = await magnet_service.update_lead_magnet(magnet, data)

    return StandardResponse(
        data=LeadMagnetResponse.model_validate(updated_magnet),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{magnet_id}",
    response_model=StandardResponse[bool],
    summary="Delete lead magnet",
)
async def delete_lead_magnet(
    magnet_id: str,
    magnet_service: LeadMagnetService = Depends(get_lead_magnet_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete lead magnet."""
    magnet = await magnet_service.get_by_id(magnet_id)

    if not magnet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead magnet not found",
        )

    await magnet_service.delete_lead_magnet(magnet)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
