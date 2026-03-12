"""
User service.
"""

from typing import Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate

logger = structlog.get_logger()


class UserService:
    """User business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User, data: UserUpdate) -> User:
        """Update user."""
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.telegram_username is not None:
            user.telegram_username = data.telegram_username

        await self.db.flush()

        logger.info(
            "user_updated",
            user_id=user.id,
        )

        return user

    async def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> tuple[list[User], int]:
        """
        List users with pagination.

        Returns:
            tuple[list[User], int]: Users and total count
        """
        query = select(User)

        if is_active is not None:
            query = query.where(User.is_active == is_active)

        # Get total count
        count_query = select(User)
        if is_active is not None:
            count_query = count_query.where(User.is_active == is_active)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def deactivate(self, user: User) -> User:
        """Deactivate user."""
        user.is_active = False
        await self.db.flush()

        logger.info(
            "user_deactivated",
            user_id=user.id,
        )

        return user

    async def update_role(
        self,
        user: User,
        roles: list[str],
        permissions: Optional[list[str]] = None,
    ) -> User:
        """Update user roles and permissions."""
        import json

        user.roles = json.dumps(roles)
        if permissions is not None:
            user.permissions = json.dumps(permissions)

        await self.db.flush()

        logger.info(
            "user_role_updated",
            user_id=user.id,
            roles=roles,
        )

        return user
