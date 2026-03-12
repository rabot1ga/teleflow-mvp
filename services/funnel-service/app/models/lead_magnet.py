"""
LeadMagnet model - lead magnets for funnels.
"""

import uuid
from typing import Optional

from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from teleflow_common.database import Base, TimestampMixin


class LeadMagnet(Base, TimestampMixin):
    """Lead magnet (freebie for subscribers)."""

    __tablename__ = "lead_magnets"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    # file, link, text, video, course_access

    # Content based on type
    file_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Delivery
    delivery_message: Mapped[str] = mapped_column(Text, nullable=False)

    # Settings
    require_subscription: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    subscription_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Stats
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)

    def __repr__(self) -> str:
        return f"<LeadMagnet(id={self.id}, name={self.name}, type={self.type})>"
