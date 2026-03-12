"""
Promotion Service models.
"""

import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PromotionTaskType(str, enum.Enum):
    """Type of promotion task."""

    PARSE = "parse"
    INVITE = "invite"
    MASSLOOK = "masslook"
    COMMENT = "comment"


class PromotionTaskStatus(str, enum.Enum):
    """Status of promotion task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PromotionTask(Base):
    """Promotion task model."""

    __tablename__ = "promotion_tasks"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    project_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    task_type: Mapped[PromotionTaskType] = mapped_column(
        Enum(PromotionTaskType),
        nullable=False,
    )
    status: Mapped[PromotionTaskStatus] = mapped_column(
        Enum(PromotionTaskStatus),
        default=PromotionTaskStatus.PENDING,
    )

    # Task configuration
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # Target info
    target_chat_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    target_chat_username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Source for parsing
    source_chat_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    source_chat_username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Filters for parsing
    parse_filters: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Stats
    total_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    processed_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    success_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    failed_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Error handling
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Dates
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<PromotionTask(id={self.id}, type={self.task_type}, status={self.status})>"


class ParsedUser(Base):
    """Parsed user from Telegram chat."""

    __tablename__ = "parsed_users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    project_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    # User info
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )
    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # User metadata
    is_bot: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    has_photo: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    last_seen_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Invite status
    is_invited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    invited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    invite_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Dates
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<ParsedUser(id={self.id}, telegram_id={self.telegram_id})>"
