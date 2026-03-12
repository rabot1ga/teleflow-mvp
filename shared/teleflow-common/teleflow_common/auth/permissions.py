"""
Permissions and RBAC.
"""

from enum import Enum


class Permission(str, Enum):
    """
    System permissions for RBAC.
    """

    # Auth & Users
    USERS_READ = "users.read"
    USERS_CREATE = "users.create"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"
    USERS_MANAGE = "users.manage"  # All user operations

    # Projects
    PROJECTS_READ = "projects.read"
    PROJECTS_CREATE = "projects.create"
    PROJECTS_UPDATE = "projects.update"
    PROJECTS_DELETE = "projects.delete"
    PROJECTS_MANAGE = "projects.manage"  # All project operations

    # Content
    ARTICLES_READ = "articles.read"
    ARTICLES_CREATE = "articles.create"
    ARTICLES_UPDATE = "articles.update"
    ARTICLES_DELETE = "articles.delete"
    ARTICLES_MODERATE = "articles.moderate"
    ARTICLES_PUBLISH = "articles.publish"

    # Sources
    SOURCES_READ = "sources.read"
    SOURCES_CREATE = "sources.create"
    SOURCES_UPDATE = "sources.update"
    SOURCES_DELETE = "sources.delete"

    # Rules
    RULES_READ = "rules.read"
    RULES_CREATE = "rules.create"
    RULES_UPDATE = "rules.update"
    RULES_DELETE = "rules.delete"

    # Publishing
    PUBLISHING_READ = "publishing.read"
    PUBLISHING_CREATE = "publishing.create"
    PUBLISHING_UPDATE = "publishing.update"
    PUBLISHING_DELETE = "publishing.delete"
    PUBLISHING_EXECUTE = "publishing.execute"

    # Targets
    TARGETS_READ = "targets.read"
    TARGETS_CREATE = "targets.create"
    TARGETS_UPDATE = "targets.update"
    TARGETS_DELETE = "targets.delete"

    # Templates
    TEMPLATES_READ = "templates.read"
    TEMPLATES_CREATE = "templates.create"
    TEMPLATES_UPDATE = "templates.update"
    TEMPLATES_DELETE = "templates.delete"

    # Funnels
    FUNNELS_READ = "funnels.read"
    FUNNELS_CREATE = "funnels.create"
    FUNNELS_UPDATE = "funnels.update"
    FUNNELS_DELETE = "funnels.delete"
    FUNNELS_MANAGE = "funnels.manage"  # All funnel operations

    # Broadcasts
    BROADCASTS_READ = "broadcasts.read"
    BROADCASTS_CREATE = "broadcasts.create"
    BROADCASTS_UPDATE = "broadcasts.update"
    BROADCASTS_DELETE = "broadcasts.delete"
    BROADCASTS_SEND = "broadcasts.send"

    # Userbots
    USERBOTS_READ = "userbots.read"
    USERBOTS_CREATE = "userbots.create"
    USERBOTS_UPDATE = "userbots.update"
    USERBOTS_DELETE = "userbots.delete"
    USERBOTS_MANAGE = "userbots.manage"  # All userbot operations

    # Proxies
    PROXIES_READ = "proxies.read"
    PROXIES_CREATE = "proxies.create"
    PROXIES_UPDATE = "proxies.update"
    PROXIES_DELETE = "proxies.delete"
    PROXIES_MANAGE = "proxies.manage"  # All proxy operations

    # Promotion
    PROMOTION_READ = "promotion.read"
    PROMOTION_CREATE = "promotion.create"
    PROMOTION_UPDATE = "promotion.update"
    PROMOTION_DELETE = "promotion.delete"
    PROMOTION_EXECUTE = "promotion.execute"

    # Analytics
    ANALYTICS_READ = "analytics.read"
    ANALYTICS_EXPORT = "analytics.export"

    # Settings
    SETTINGS_READ = "settings.read"
    SETTINGS_UPDATE = "settings.update"

    # AI Operations
    AI_USE = "ai.use"


class Role(str, Enum):
    """
    System roles with associated permissions.
    """

    SUPER_ADMIN = "super_admin"  # Full access
    ADMIN = "admin"  # Project management
    CHIEF_EDITOR = "chief_editor"  # Editorial policy
    EDITOR = "editor"  # Moderation
    ANALYST = "analyst"  # Read-only analytics
    OPERATOR = "operator"  # Promotion operations
    USER = "user"  # Basic user


# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.SUPER_ADMIN: list(Permission),  # All permissions
    Role.ADMIN: [
        Permission.USERS_MANAGE,
        Permission.PROJECTS_MANAGE,
        Permission.SETTINGS_READ,
        Permission.SETTINGS_UPDATE,
        Permission.ANALYTICS_READ,
        Permission.ANALYTICS_EXPORT,
    ],
    Role.CHIEF_EDITOR: [
        Permission.ARTICLES_READ,
        Permission.ARTICLES_CREATE,
        Permission.ARTICLES_UPDATE,
        Permission.ARTICLES_DELETE,
        Permission.ARTICLES_MODERATE,
        Permission.ARTICLES_PUBLISH,
        Permission.SOURCES_READ,
        Permission.SOURCES_CREATE,
        Permission.SOURCES_UPDATE,
        Permission.SOURCES_DELETE,
        Permission.RULES_READ,
        Permission.RULES_CREATE,
        Permission.RULES_UPDATE,
        Permission.RULES_DELETE,
        Permission.PUBLISHING_READ,
        Permission.PUBLISHING_CREATE,
        Permission.PUBLISHING_UPDATE,
        Permission.PUBLISHING_DELETE,
    ],
    Role.EDITOR: [
        Permission.ARTICLES_READ,
        Permission.ARTICLES_UPDATE,
        Permission.ARTICLES_MODERATE,
        Permission.SOURCES_READ,
    ],
    Role.ANALYST: [
        Permission.ANALYTICS_READ,
        Permission.ANALYTICS_EXPORT,
        Permission.ARTICLES_READ,
        Permission.USERS_READ,
        Permission.PROJECTS_READ,
    ],
    Role.OPERATOR: [
        Permission.USERBOTS_MANAGE,
        Permission.PROMOTION_EXECUTE,
        Permission.PROXIES_MANAGE,
        Permission.ANALYTICS_READ,
    ],
    Role.USER: [
        Permission.ARTICLES_READ,
        Permission.ANALYTICS_READ,
    ],
}


def get_permissions_for_role(role: Role) -> list[Permission]:
    """Get all permissions for a role."""
    return ROLE_PERMISSIONS.get(role, [])


def check_permission(role: Role, permission: Permission) -> bool:
    """Check if a role has a specific permission."""
    permissions = get_permissions_for_role(role)
    return permission in permissions
