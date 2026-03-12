"""Promotion Service models."""

from app.models.promotion import ParsedUser, PromotionTask, PromotionTaskStatus, PromotionTaskType

__all__ = [
    "PromotionTask",
    "PromotionTaskType",
    "PromotionTaskStatus",
    "ParsedUser",
]
