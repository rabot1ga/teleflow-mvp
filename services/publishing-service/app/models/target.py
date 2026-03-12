"""
PublishTarget model - Telegram channels for publishing.
"""

import uuid
from datetime import time
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Integer, String, Text, Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class PublishTarget(Base, TimestampMixin):
    """Publish target (Telegram channel)."""

    __tablename__ = "publish_targets"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    telegram_chat_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Rate limiting
    min_interval_seconds: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
    max_per_hour: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    max_per_day: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    # Working hours
    working_hours_start: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    working_hours_end: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow", nullable=False)

    # Defaults
    categories: Mapped[list] = mapped_column(ARRAY(String), default=list, nullable=False)
    default_template_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_published_at: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    # Relationships
    jobs: Mapped[list["PublishJob"]] = relationship(  # noqa: F821
        "PublishJob",
        back_populates="target",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PublishTarget(id={self.id}, name={self.name}, chat_id={self.telegram_chat_id})>"
