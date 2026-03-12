"""
Moderation models.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class ModerationBatch(Base, TimestampMixin):
    """Batch of articles for moderation."""

    __tablename__ = "moderation_batches"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    moderator_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    strategy: Mapped[str] = mapped_column(String(50), default="by_priority", nullable=False)
    article_ids: Mapped[list] = mapped_column(ARRAY(String(36)), nullable=False)
    telegram_message_ids: Mapped[list] = mapped_column(ARRAY(BigInteger), default=list)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )  # pending, in_progress, completed
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<ModerationBatch(id={self.id}, status={self.status}, articles={len(self.article_ids)})>"


class AutomationRule(Base, TimestampMixin):
    """Automation rule for content moderation."""

    __tablename__ = "automation_rules"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conditions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Example: {"operator": "AND", "rules": [{"field": "quality_score", "op": "gte", "value": 0.8}]}
    actions: Mapped[list] = mapped_column(JSONB, nullable=False)
    # Example: [{"type": "auto_approve", "params": {}}, {"type": "add_tags", "params": {"tags": ["verified"]}}]
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)

    def __repr__(self) -> str:
        return f"<AutomationRule(id={self.id}, name={self.name}, active={self.is_active})>"
