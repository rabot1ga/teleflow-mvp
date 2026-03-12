"""Pydantic schemas for Userbot API."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class AccountStatusEnum(str, Enum):
    """Account status."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    BANNED = "banned"
    NEEDS_AUTH = "needs_auth"
    NEEDS_2FA = "needs_2fa"


class ProxyTypeEnum(str, Enum):
    """Proxy type."""

    MTProto = "mtproto"
    SOCKS5 = "socks5"
    HTTP = "http"


# ==================== Account Schemas ====================


class UserbotAccountBase(BaseModel):
    """Base schema for userbot account."""

    name: str = Field(..., min_length=1, max_length=255)
    project_id: UUID


class UserbotAccountCreate(UserbotAccountBase):
    """Schema for creating account."""

    pass


class UserbotAccountUpdate(BaseModel):
    """Schema for updating account."""

    name: str | None = Field(None, min_length=1, max_length=255)
    is_warming_enabled: bool | None = None


class UserbotAccountResponse(UserbotAccountBase):
    """Schema for account response."""

    id: UUID
    phone_number: str | None = None
    telegram_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    status: AccountStatusEnum
    is_warming_enabled: bool = False
    warming_day: int = 0
    is_online: bool = False
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserbotAccountAuthRequest(BaseModel):
    """Schema for sending auth code."""

    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")


class UserbotAccountVerifyRequest(BaseModel):
    """Schema for verifying auth code."""

    code: str = Field(..., min_length=4, max_length=10)


class UserbotAccount2FARequest(BaseModel):
    """Schema for 2FA password."""

    password: str = Field(..., min_length=1)


# ==================== Proxy Schemas ====================


class ProxyBase(BaseModel):
    """Base schema for proxy."""

    name: str = Field(..., min_length=1, max_length=255)
    account_id: UUID
    proxy_type: ProxyTypeEnum
    hostname: str
    port: int = Field(..., gt=0, lt=65536)
    username: str | None = None
    password: str | None = None
    secret: str | None = None


class ProxyCreate(ProxyBase):
    """Schema for creating proxy."""

    pass


class ProxyUpdate(BaseModel):
    """Schema for updating proxy."""

    name: str | None = Field(None, min_length=1, max_length=255)
    hostname: str | None = None
    port: int | None = Field(None, gt=0, lt=65536)
    username: str | None = None
    password: str | None = None
    secret: str | None = None
    is_active: bool | None = None


class ProxyResponse(ProxyBase):
    """Schema for proxy response."""

    id: UUID
    is_active: bool = True
    is_working: bool | None = None
    last_checked_at: datetime | None = None
    response_time_ms: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProxyCheckResponse(BaseModel):
    """Schema for proxy check result."""

    is_working: bool
    response_time_ms: int | None = None
    error: str | None = None


# ==================== Session Schemas ====================


class SessionDataResponse(BaseModel):
    """Schema for session data response."""

    id: UUID
    account_id: UUID
    dc_id: int | None = None
    server: str | None = None
    port: int | None = None
    is_valid: bool = True
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Warming Schemas ====================


class WarmingSchedule(BaseModel):
    """Warming schedule for account."""

    day: int
    actions: list[str]
    min_delay_minutes: int
    max_delay_minutes: int


class WarmingStatusResponse(BaseModel):
    """Warming status for account."""

    account_id: UUID
    is_enabled: bool
    current_day: int
    started_at: datetime | None = None
    last_action_at: datetime | None = None
    next_action_at: datetime | None = None
    total_actions: int = 0
