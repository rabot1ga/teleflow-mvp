"""
Project endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.project import (
    ProjectCreate,
    ProjectMemberAdd,
    ProjectMemberResponse,
    ProjectResponse,
)
from app.services.project_service import ProjectService
from app.dependencies import get_async_session
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db=Depends(get_async_session)) -> ProjectService:
    """Get project service instance."""
    return ProjectService(db)


@router.post(
    "",
    response_model=StandardResponse[ProjectResponse],
    summary="Create project",
)
async def create_project(
    data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ProjectResponse]:
    """Create a new project."""
    project = await project_service.create_project(
        data=data,
        owner_id=current_user["user_id"],
    )

    return StandardResponse(
        data=ProjectResponse.model_validate(project),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[list[ProjectResponse]],
    summary="List user projects",
)
async def list_projects(
    project_service: ProjectService = Depends(get_project_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[list[ProjectResponse]]:
    """List all projects for current user."""
    projects = await project_service.get_user_projects(current_user["user_id"])

    return StandardResponse(
        data=[ProjectResponse.model_validate(p) for p in projects],
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{project_id}",
    response_model=StandardResponse[ProjectResponse],
    summary="Get project by ID",
)
async def get_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[ProjectResponse]:
    """Get project by ID."""
    project = await project_service.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return StandardResponse(
        data=ProjectResponse.model_validate(project),
        meta=ResponseMeta(request_id=""),
    )


@router.post(
    "/{project_id}/members",
    response_model=StandardResponse[ProjectMemberResponse],
    summary="Add member to project",
)
async def add_member(
    project_id: str,
    data: ProjectMemberAdd,
    project_service: ProjectService = Depends(get_project_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[ProjectMemberResponse]:
    """Add member to project."""
    project = await project_service.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    member = await project_service.add_member(project, data)

    return StandardResponse(
        data=ProjectMemberResponse.model_validate(member),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{project_id}/members/{user_id}",
    response_model=StandardResponse[bool],
    summary="Remove member from project",
)
async def remove_member(
    project_id: str,
    user_id: str,
    project_service: ProjectService = Depends(get_project_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[bool]:
    """Remove member from project."""
    project = await project_service.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    await project_service.remove_member(project, user_id)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
