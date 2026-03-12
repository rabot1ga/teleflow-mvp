"""
Authentication service.
"""

import uuid
from datetime import datetime
from typing import Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import RegisterRequest
from teleflow_common.auth.jwt import JWTManager, PasswordManager

logger = structlog.get_logger()


class AuthService:
    """Authentication business logic."""

    def __init__(self, db: AsyncSession, jwt_manager: JWTManager):
        self.db = db
        self.jwt_manager = jwt_manager
        self.password_manager = PasswordManager()

    async def register(self, data: RegisterRequest) -> User:
        """Register a new user."""
        # Check if user exists
        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Create user
        user = User(
            email=data.email,
            password_hash=self.password_manager.hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            roles='["user"]',
            permissions='[]',
        )

        self.db.add(user)
        await self.db.flush()

        logger.info(
            "user_registered",
            user_id=user.id,
            email=user.email,
        )

        return user

    async def login(self, email: str, password: str) -> tuple[User, dict]:
        """
        Login user and return user + tokens.

        Returns:
            tuple[User, dict]: User and token data (access_token, refresh_token)
        """
        # Find user
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is deactivated")

        # Verify password
        if not self.password_manager.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.db.flush()

        # Create tokens
        tokens = self.create_tokens(user)

        logger.info(
            "user_logged_in",
            user_id=user.id,
            email=user.email,
        )

        return user, tokens

    async def refresh_tokens(
        self, refresh_token: str
    ) -> tuple[User, dict]:
        """Refresh access and refresh tokens."""
        try:
            # Verify refresh token
            payload = self.jwt_manager.verify_refresh_token(refresh_token)
            user_id = payload.get("sub")

            if not user_id:
                raise ValueError("Invalid token")

            # Get user
            result = await self.db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user or not user.is_active:
                raise ValueError("User not found or inactive")

            # Create new tokens
            tokens = self.create_tokens(user)

            logger.info(
                "tokens_refreshed",
                user_id=user.id,
            )

            return user, tokens

        except Exception as e:
            logger.warning("token_refresh_failed", error=str(e))
            raise ValueError("Invalid refresh token")

    def create_tokens(self, user: User) -> dict:
        """Create JWT tokens for user."""
        access_token = self.jwt_manager.create_access_token(
            subject=user.id,
            extra_data={
                "email": user.email,
                "roles": user.roles,
                "permissions": user.permissions,
            },
        )
        refresh_token = self.jwt_manager.create_refresh_token(subject=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def logout(self, user: User, refresh_token: str) -> None:
        """
        Logout user (add refresh token to blacklist).

        Note: In production, store blacklisted tokens in Redis with TTL.
        """
        # For MVP, we just log the action
        # In production: await redis.setex(f"blacklist:{refresh_token}", ttl, 1)
        logger.info(
            "user_logged_out",
            user_id=user.id,
        )
