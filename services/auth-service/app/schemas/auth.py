"""
Auth-related schemas.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Registration request schema."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Token refresh request schema."""

    refresh_token: str


class TokenData(BaseModel):
    """Token data schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Login response schema."""

    success: bool = True
    data: TokenData
    meta: dict | None = None
