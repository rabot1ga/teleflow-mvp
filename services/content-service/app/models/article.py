"""
Article model - represents aggregated content items.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class Article(Base, TimestampMixin):
    """Article/material model."""

    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    source_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Content
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Metadata
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="ru", nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Scores
    quality_score: Mapped[float] = mapped_column(default=0.0, nullable=False)  # 0.0 to 1.0
    priority_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False)  # 0 to 100

    # Dedup
    url_hash: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True, index=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    simhash: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
        index=True,
    )  # pending, approved, rejected, duplicate, scheduled, published

    # Moderation
    moderated_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    moderated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rejection_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Publication
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    publish_target_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    telegram_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Dates
    original_pub_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Batch moderation
    moderation_batch_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("moderation_batches.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    source: Mapped[Optional["Source"]] = relationship(  # noqa: F821
        "Source",
        back_populates="articles",
    )
    versions: Mapped[list["ArticleVersion"]] = relationship(  # noqa: F821
        "ArticleVersion",
        back_populates="article",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title={self.title[:50]}..., status={self.status})>"
