"""
Publish Templates API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.template import PublishTemplateCreate, PublishTemplateList, PublishTemplateResponse, PublishTemplateUpdate
from app.services.template_service import PublishTemplateService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/templates", tags=["Publish Templates"])


def get_template_service(db=Depends(get_async_session)) -> PublishTemplateService:
    """Get template service instance."""
    return PublishTemplateService(db)


@router.post(
    "",
    response_model=StandardResponse[PublishTemplateResponse],
    summary="Create publish template",
)
async def create_template(
    data: PublishTemplateCreate,
    template_service: PublishTemplateService = Depends(get_template_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTemplateResponse]:
    """Create a new publish template."""
    template = await template_service.create_template(data)

    return StandardResponse(
        data=PublishTemplateResponse.model_validate(template),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[PublishTemplateList],
    summary="List publish templates",
)
async def list_templates(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = None,
    template_service: PublishTemplateService = Depends(get_template_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTemplateList]:
    """List publish templates with pagination."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    templates, total = await template_service.list_templates(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        is_active=is_active,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=PublishTemplateList(
            items=[PublishTemplateResponse.model_validate(t) for t in templates],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{template_id}",
    response_model=StandardResponse[PublishTemplateResponse],
    summary="Get publish template by ID",
)
async def get_template(
    template_id: str,
    template_service: PublishTemplateService = Depends(get_template_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTemplateResponse]:
    """Get publish template by ID."""
    template = await template_service.get_by_id(template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )

    return StandardResponse(
        data=PublishTemplateResponse.model_validate(template),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{template_id}",
    response_model=StandardResponse[PublishTemplateResponse],
    summary="Update publish template",
)
async def update_template(
    template_id: str,
    data: PublishTemplateUpdate,
    template_service: PublishTemplateService = Depends(get_template_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishTemplateResponse]:
    """Update publish template."""
    template = await template_service.get_by_id(template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )

    updated_template = await template_service.update_template(template, data)

    return StandardResponse(
        data=PublishTemplateResponse.model_validate(updated_template),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{template_id}",
    response_model=StandardResponse[bool],
    summary="Delete publish template",
)
async def delete_template(
    template_id: str,
    template_service: PublishTemplateService = Depends(get_template_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete publish template."""
    template = await template_service.get_by_id(template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )

    await template_service.delete_template(template)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
