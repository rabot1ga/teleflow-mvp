"""Promotion Service schemas."""

from app.schemas.promotion import (
    CommentConfig,
    InviteConfig,
    MasslookConfig,
    ParseConfig,
    ParsedUserFilter,
    ParsedUserResponse,
    PromotionTaskCreate,
    PromotionTaskResponse,
    PromotionTaskStatusEnum,
    PromotionTaskTypeEnum,
    PromotionTaskUpdate,
)

__all__ = [
    "PromotionTaskCreate",
    "PromotionTaskUpdate",
    "PromotionTaskResponse",
    "PromotionTaskTypeEnum",
    "PromotionTaskStatusEnum",
    "ParsedUserResponse",
    "ParsedUserFilter",
    "ParseConfig",
    "InviteConfig",
    "MasslookConfig",
    "CommentConfig",
]
