"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RegisterRequest,
    TokenData,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.dependencies import get_async_session
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db=Depends(get_async_session)) -> AuthService:
    """Get auth service instance."""
    from teleflow_common.auth.jwt import AuthSettings, JWTManager

    auth_settings = AuthSettings()
    jwt_manager = JWTManager(auth_settings)
    return AuthService(db, jwt_manager)


@router.post(
    "/register",
    response_model=StandardResponse[dict],
    summary="Register new user",
)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> StandardResponse[dict]:
    """Register a new user account."""
    try:
        user = await auth_service.register(data)
        tokens = auth_service.create_tokens(user)

        return StandardResponse(
            data={
                "user": UserResponse.model_validate(user),
                **tokens,
            },
            meta=ResponseMeta(request_id=""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=StandardResponse[dict],
    summary="Login user",
)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> StandardResponse[dict]:
    """Login with email and password."""
    try:
        user, tokens = await auth_service.login(data.email, data.password)

        return StandardResponse(
            data={
                "user": UserResponse.model_validate(user),
                **tokens,
            },
            meta=ResponseMeta(request_id=""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/refresh",
    response_model=StandardResponse[dict],
    summary="Refresh tokens",
)
async def refresh_tokens(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> StandardResponse[dict]:
    """Refresh access and refresh tokens."""
    try:
        user, tokens = await auth_service.refresh_tokens(data.refresh_token)

        return StandardResponse(
            data=tokens,
            meta=ResponseMeta(request_id=""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/logout",
    response_model=StandardResponse[bool],
    summary="Logout user",
)
async def logout(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Logout user and blacklist refresh token."""
    user = await auth_service.get_user_by_id(current_user["user_id"])
    if user:
        await auth_service.logout(user, data.refresh_token)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))


@router.get(
    "/me",
    response_model=StandardResponse[UserResponse],
    summary="Get current user",
)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(
        lambda db=Depends(get_async_session): UserService(db)
    ),
) -> StandardResponse[UserResponse]:
    """Get current user profile."""
    user = await user_service.get_by_id(current_user["user_id"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return StandardResponse(
        data=UserResponse.model_validate(user),
        meta=ResponseMeta(request_id=""),
    )
