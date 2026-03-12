"""
Broadcast model - mass messaging campaigns.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from teleflow_common.database import Base, TimestampMixin


class Broadcast(Base, TimestampMixin):
    """Broadcast campaign."""

    __tablename__ = "broadcasts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Content
    message_type: Mapped[str] = mapped_column(String(20), default="text", nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    message_media_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    buttons: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Recipients filter
    recipient_filter: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # {"type": "all"} | {"type": "funnel", "funnel_id": "...", "status": "completed"}
    # {"type": "tags", "tags": ["premium"], "operator": "any"}
    # {"type": "list", "user_ids": [...]}

    # Schedule
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        nullable=False,
    )  # draft, scheduled, running, paused, completed, cancelled

    # Stats
    total_recipients: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    delivered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Settings
    send_rate: Mapped[int] = mapped_column(Integer, default=30, nullable=False)  # msg/sec

    # Execution
    created_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Broadcast(id={self.id}, name={self.name}, status={self.status})>"
