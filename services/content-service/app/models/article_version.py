"""
ArticleVersion model - tracks article edit history.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class ArticleVersion(Base, TimestampMixin):
    """Article version history."""

    __tablename__ = "article_versions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    article_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    change_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # created, edited, ai_rewritten

    # Relationships
    article: Mapped["Article"] = relationship(  # noqa: F821
        "Article",
        back_populates="versions",
    )

    def __repr__(self) -> str:
        return f"<ArticleVersion(id={self.id}, article_id={self.article_id}, type={self.change_type})>"
