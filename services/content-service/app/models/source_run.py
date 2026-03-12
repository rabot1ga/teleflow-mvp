"""
SourceRun model - tracks source fetch history.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class SourceRun(Base, TimestampMixin):
    """Source fetch run history."""

    __tablename__ = "source_runs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    source_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # running, completed, failed
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    articles_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_new: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_duplicate: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    source: Mapped["Source"] = relationship(  # noqa: F821
        "Source",
        back_populates="runs",
    )

    def __repr__(self) -> str:
        return f"<SourceRun(id={self.id}, source_id={self.source_id}, status={self.status})>"
