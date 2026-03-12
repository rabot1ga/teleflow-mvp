"""Pydantic schemas for Promotion API."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PromotionTaskTypeEnum(str, Enum):
    """Promotion task type."""

    PARSE = "parse"
    INVITE = "invite"
    MASSLOOK = "masslook"
    COMMENT = "comment"


class PromotionTaskStatusEnum(str, Enum):
    """Promotion task status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ==================== Task Schemas ====================


class PromotionTaskBase(BaseModel):
    """Base schema for promotion task."""

    name: str = Field(..., min_length=1, max_length=255)
    project_id: UUID
    task_type: PromotionTaskTypeEnum


class PromotionTaskCreate(PromotionTaskBase):
    """Schema for creating promotion task."""

    target_chat_id: str | None = None
    target_chat_username: str | None = None
    source_chat_id: str | None = None
    source_chat_username: str | None = None
    parse_filters: dict | None = None
    config: dict = Field(default_factory=dict)


class PromotionTaskUpdate(BaseModel):
    """Schema for updating promotion task."""

    name: str | None = Field(None, min_length=1, max_length=255)
    config: dict | None = None


class PromotionTaskResponse(PromotionTaskBase):
    """Schema for task response."""

    id: UUID
    status: PromotionTaskStatusEnum
    target_chat_id: str | None = None
    target_chat_username: str | None = None
    source_chat_id: str | None = None
    source_chat_username: str | None = None
    parse_filters: dict | None = None
    config: dict = Field(default_factory=dict)
    total_count: int = 0
    processed_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Parsed User Schemas ====================


class ParsedUserResponse(BaseModel):
    """Schema for parsed user response."""

    id: UUID
    task_id: UUID
    project_id: UUID
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    is_bot: bool = False
    is_premium: bool = False
    has_photo: bool = False
    last_seen_days: int | None = None
    is_invited: bool = False
    invited_at: datetime | None = None
    invite_error: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ParsedUserFilter(BaseModel):
    """Filter for parsed users."""

    is_invited: bool | None = None
    has_photo: bool | None = None
    is_premium: bool | None = None
    is_bot: bool | None = None
    last_seen_days_max: int | None = None


# ==================== Parse Config Schemas ====================


class ParseConfig(BaseModel):
    """Configuration for parsing task."""

    limit: int = Field(default=1000, ge=1, le=10000)
    offset: int = Field(default=0, ge=0)
    filter_active_days: int | None = Field(None, ge=1)
    filter_has_photo: bool | None = None
    filter_is_premium: bool | None = None
    filter_is_bot: bool = False


class InviteConfig(BaseModel):
    """Configuration for invite task."""

    max_invites_per_account: int = Field(default=50, ge=1, le=100)
    delay_between_invites_sec: int = Field(default=30, ge=10, le=300)
    userbot_account_ids: list[UUID] = Field(default_factory=list)


class MasslookConfig(BaseModel):
    """Configuration for masslooking task."""

    stories_to_look: int = Field(default=5, ge=1, le=50)
    delay_between_views_sec: int = Field(default=5, ge=1, le=60)
    userbot_account_ids: list[UUID] = Field(default_factory=list)


class CommentConfig(BaseModel):
    """Configuration for commenting task."""

    comment_text: str = Field(..., min_length=1, max_length=4096)
    comments_per_account: int = Field(default=10, ge=1, le=100)
    delay_between_comments_sec: int = Field(default=60, ge=30, le=600)
    userbot_account_ids: list[UUID] = Field(default_factory=list)
