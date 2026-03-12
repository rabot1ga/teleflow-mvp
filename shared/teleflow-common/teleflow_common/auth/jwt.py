"""
Auth module for TeleFlow services.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from teleflow_common.config.settings import BaseSettings


class AuthSettings(BaseSettings):
    """Authentication settings."""

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_MINUTES: int = 15
    JWT_REFRESH_TOKEN_DAYS: int = 7


class PasswordManager:
    """Password hashing and verification."""

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return self._context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return self._context.verify(plain_password, hashed_password)


class JWTManager:
    """JWT token creation and verification."""

    def __init__(self, settings: AuthSettings):
        self.settings = settings
        self.password_manager = PasswordManager()

    def create_access_token(
        self, subject: str, extra_data: Optional[dict] = None
    ) -> str:
        """Create JWT access token."""
        expire = datetime.utcnow() + timedelta(
            minutes=self.settings.JWT_ACCESS_TOKEN_MINUTES
        )
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
        }
        if extra_data:
            to_encode.update(extra_data)

        return jwt.encode(
            to_encode,
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def create_refresh_token(self, subject: str) -> str:
        """Create JWT refresh token."""
        expire = datetime.utcnow() + timedelta(
            days=self.settings.JWT_REFRESH_TOKEN_DAYS
        )
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
        }
        return jwt.encode(
            to_encode,
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict:
        """Decode and verify JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET,
                algorithms=[self.settings.JWT_ALGORITHM],
            )
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def verify_access_token(self, token: str) -> dict:
        """Verify access token and return payload."""
        payload = self.decode_token(token)
        if payload.get("type") != "access":
            raise ValueError("Token is not an access token")
        return payload

    def verify_refresh_token(self, token: str) -> dict:
        """Verify refresh token and return payload."""
        payload = self.decode_token(token)
        if payload.get("type") != "refresh":
            raise ValueError("Token is not a refresh token")
        return payload
