"""
FunnelUser model - users in funnels.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class FunnelUser(Base, TimestampMixin):
    """User in a funnel."""

    __tablename__ = "funnel_users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    funnel_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("funnels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    telegram_user_id: Mapped[int] = mapped_column(nullable=False, index=True)

    current_step_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("funnel_steps.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    # active, paused, completed, dropped

    # Data
    user_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[list] = mapped_column(ARRAY(String), default=list)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Dates
    entered_at: Mapped[datetime] = mapped_column(nullable=False)
    last_action_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    next_step_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, index=True)

    # Relationships
    funnel: Mapped["Funnel"] = relationship(  # noqa: F821
        "Funnel",
        back_populates="users",
    )

    def __repr__(self) -> str:
        return f"<FunnelUser(id={self.id}, funnel_id={self.funnel_id}, tg_user={self.telegram_user_id})>"
