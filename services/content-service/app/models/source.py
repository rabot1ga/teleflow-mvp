"""
Source model - represents content sources (RSS, API, scraper, etc.)
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class Source(Base, TimestampMixin):
    """Content source model."""

    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # rss, json_api, scraper, webhook, telegram
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    fetch_interval_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    default_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    default_tags: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    priority_boost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # -10 to 10
    reputation: Mapped[float] = mapped_column(default=0.5, nullable=False)  # 0.0 to 1.0
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_fetch_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    articles: Mapped[list["Article"]] = relationship(  # noqa: F821
        "Article",
        back_populates="source",
        cascade="all, delete-orphan",
    )
    runs: Mapped[list["SourceRun"]] = relationship(  # noqa: F821
        "SourceRun",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Source(id={self.id}, name={self.name}, type={self.source_type})>"
