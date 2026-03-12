"""
Auth module.
"""

from teleflow_common.auth.dependencies import (
    get_auth_settings,
    get_current_user,
    get_jwt_manager,
    require_permission,
    require_role,
)
from teleflow_common.auth.jwt import AuthSettings, JWTManager, PasswordManager
from teleflow_common.auth.permissions import (
    Permission,
    Role,
    ROLE_PERMISSIONS,
    check_permission,
    get_permissions_for_role,
)

__all__ = [
    # Dependencies
    "get_auth_settings",
    "get_current_user",
    "get_jwt_manager",
    "require_permission",
    "require_role",
    # JWT
    "AuthSettings",
    "JWTManager",
    "PasswordManager",
    # Permissions
    "Permission",
    "Role",
    "ROLE_PERMISSIONS",
    "check_permission",
    "get_permissions_for_role",
]
