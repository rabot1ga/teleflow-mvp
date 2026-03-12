"""
Auth dependencies for FastAPI.
"""

from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from teleflow_common.auth.jwt import AuthSettings, JWTManager

# Reusable security scheme
http_bearer = HTTPBearer(auto_error=False)


def get_auth_settings() -> AuthSettings:
    """Get auth settings from environment."""
    return AuthSettings()


def get_jwt_manager(settings: AuthSettings = Depends(get_auth_settings)) -> JWTManager:
    """Get JWT manager instance."""
    return JWTManager(settings)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> dict:
    """
    Get current user from JWT token.

    Usage:
        @router.get("/me")
        async def get_me(user: dict = Depends(get_current_user)):
            return user
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt_manager.verify_access_token(credentials.credentials)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", []),
            "permissions": payload.get("permissions", []),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_permission(permission: str):
    """
    Dependency factory that requires specific permission.

    Usage:
        @router.get("/admin")
        async def admin_endpoint(
            user: dict = Depends(require_permission("admin.manage"))
        ):
            return {"message": "Admin access"}
    """

    async def permission_checker(
        user: dict = Depends(get_current_user),
    ) -> dict:
        user_permissions = user.get("permissions", [])
        user_roles = user.get("roles", [])

        # Check if user has the permission directly or through role
        if permission not in user_permissions and permission not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}",
            )

        return user

    return permission_checker


def require_role(role: str):
    """
    Dependency factory that requires specific role.

    Usage:
        @router.get("/admin")
        async def admin_endpoint(
            user: dict = Depends(require_role("admin"))
        ):
            return {"message": "Admin access"}
    """

    async def role_checker(
        user: dict = Depends(get_current_user),
    ) -> dict:
        user_roles = user.get("roles", [])

        if role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required role: {role}",
            )

        return user

    return role_checker
