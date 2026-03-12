"""
Internal endpoints for service-to-service communication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import AuthService
from app.dependencies import get_async_session
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/internal", tags=["Internal"])

http_bearer = HTTPBearer(auto_error=False)


def get_auth_service(db=Depends(get_async_session)) -> AuthService:
    """Get auth service instance."""
    from teleflow_common.auth.jwt import AuthSettings, JWTManager

    auth_settings = AuthSettings()
    jwt_manager = JWTManager(auth_settings)
    return AuthService(db, jwt_manager)


@router.post(
    "/auth/validate-token",
    response_model=StandardResponse[dict],
    summary="Validate JWT token (internal)",
)
async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(get_auth_service),
) -> StandardResponse[dict]:
    """Validate JWT token and return user data."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
        )

    try:
        payload = auth_service.jwt_manager.verify_access_token(credentials.credentials)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = await auth_service.get_user_by_id(user_id)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        return StandardResponse(
            data={
                "user_id": user.id,
                "email": user.email,
                "roles": user.roles,
                "permissions": user.permissions,
                "is_active": user.is_active,
            },
            meta=ResponseMeta(request_id=""),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get(
    "/auth/users/{user_id}",
    response_model=StandardResponse[dict],
    summary="Get user by ID (internal)",
)
async def get_user_internal(
    user_id: str,
    auth_service: AuthService = Depends(get_auth_service),
) -> StandardResponse[dict]:
    """Get user by ID for internal service calls."""
    user = await auth_service.get_user_by_id(user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return StandardResponse(
        data={
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        meta=ResponseMeta(request_id=""),
    )
