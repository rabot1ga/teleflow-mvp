"""Analytics Service models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AnalyticsEvent(Base):
    """Raw analytics event."""

    __tablename__ = "analytics_events"

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

    # Event type
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )  # article.created, article.published, funnel.user_entered, etc.

    # Event data
    entity_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )  # article, funnel, broadcast, etc.
    entity_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    # Event payload
    payload: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # User info
    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    # Timestamps
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<AnalyticsEvent(id={self.id}, type={self.event_type})>"


class AnalyticsDaily(Base):
    """Daily aggregated analytics."""

    __tablename__ = "analytics_daily"

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
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # Content stats
    articles_created: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    articles_approved: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    articles_published: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    articles_rejected: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Funnel stats
    funnel_entries: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    funnel_completions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Broadcast stats
    broadcasts_sent: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    messages_delivered: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Promotion stats
    users_parsed: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    users_invited: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Userbot stats
    userbot_actions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # AI stats
    ai_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    ai_tokens_used: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Dates
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
        return f"<AnalyticsDaily(project_id={self.project_id}, date={self.date})>"
