"""
User management endpoints (admin).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies import get_async_session
from teleflow_common.auth.dependencies import get_current_user, require_permission
from teleflow_common.schemas.responses import (
    PaginatedResponse,
    ResponseMeta,
    StandardResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db=Depends(get_async_session)) -> UserService:
    """Get user service instance."""
    return UserService(db)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="List users",
)
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = None,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> PaginatedResponse[UserResponse]:
    """List all users (admin only)."""
    skip = (page - 1) * per_page
    users, total = await user_service.list_users(
        skip=skip,
        limit=per_page,
        is_active=is_active,
    )

    return PaginatedResponse.create(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        per_page=per_page,
        request_id="",
    )


@router.get(
    "/{user_id}",
    response_model=StandardResponse[UserResponse],
    summary="Get user by ID",
)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[UserResponse]:
    """Get user by ID (admin only)."""
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return StandardResponse(
        data=UserResponse.model_validate(user),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{user_id}",
    response_model=StandardResponse[UserResponse],
    summary="Update user",
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[UserResponse]:
    """Update user (admin only)."""
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    updated_user = await user_service.update(user, data)

    return StandardResponse(
        data=UserResponse.model_validate(updated_user),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{user_id}",
    response_model=StandardResponse[bool],
    summary="Deactivate user",
)
async def deactivate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),  # noqa: ARG001
) -> StandardResponse[bool]:
    """Deactivate user (admin only)."""
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await user_service.deactivate(user)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))
