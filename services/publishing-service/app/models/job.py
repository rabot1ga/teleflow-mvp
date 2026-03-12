"""
PublishJob model - publishing tasks.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class PublishJob(Base, TimestampMixin):
    """Publish job (task)."""

    __tablename__ = "publish_jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    article_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    target_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("publish_targets.id", ondelete="CASCADE"),
        nullable=False,
    )
    template_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("publish_templates.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Schedule
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
        index=True,
    )  # pending, scheduled, publishing, published, failed, cancelled

    # Result
    telegram_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    # Relationships
    target: Mapped["PublishTarget"] = relationship(  # noqa: F821
        "PublishTarget",
        back_populates="jobs",
    )

    def __repr__(self) -> str:
        return f"<PublishJob(id={self.id}, article_id={self.article_id}, status={self.status})>"
