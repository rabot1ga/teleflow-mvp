"""
Sources API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.source import SourceCreate, SourceList, SourceResponse, SourceUpdate
from app.services.source_service import SourceService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/sources", tags=["Sources"])


def get_source_service(db=Depends(get_async_session)) -> SourceService:
    """Get source service instance."""
    return SourceService(db)


@router.post(
    "",
    response_model=StandardResponse[SourceResponse],
    summary="Create source",
)
async def create_source(
    data: SourceCreate,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[SourceResponse]:
    """Create a new content source."""
    source = await source_service.create_source(data)

    return StandardResponse(
        data=SourceResponse.model_validate(source),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[SourceList],
    summary="List sources",
)
async def list_sources(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = None,
    source_type: str | None = None,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[SourceList]:
    """List sources with pagination."""
    skip = (page - 1) * per_page
    sources, total = await source_service.list_sources(
        project_id=current_user.get("project_id", ""),
        skip=skip,
        limit=per_page,
        is_active=is_active,
        source_type=source_type,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=SourceList(
            items=[SourceResponse.model_validate(s) for s in sources],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{source_id}",
    response_model=StandardResponse[SourceResponse],
    summary="Get source by ID",
)
async def get_source(
    source_id: str,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[SourceResponse]:
    """Get source by ID."""
    source = await source_service.get_by_id(source_id)

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    return StandardResponse(
        data=SourceResponse.model_validate(source),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{source_id}",
    response_model=StandardResponse[SourceResponse],
    summary="Update source",
)
async def update_source(
    source_id: str,
    data: SourceUpdate,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[SourceResponse]:
    """Update source."""
    source = await source_service.get_by_id(source_id)

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    updated_source = await source_service.update_source(source, data)

    return StandardResponse(
        data=SourceResponse.model_validate(updated_source),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{source_id}",
    response_model=StandardResponse[bool],
    summary="Delete source",
)
async def delete_source(
    source_id: str,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete source."""
    source = await source_service.get_by_id(source_id)

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    await source_service.delete_source(source)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))


@router.post(
    "/{source_id}/fetch",
    response_model=StandardResponse[bool],
    summary="Fetch source now",
)
async def fetch_source_now(
    source_id: str,
    source_service: SourceService = Depends(get_source_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Trigger immediate source fetch."""
    source = await source_service.get_by_id(source_id)

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    # Trigger Celery task
    from app.tasks import fetch_source
    fetch_source.delay(source_id)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
