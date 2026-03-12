"""
CRMSegment model - user segments for targeting.
"""

import uuid
from typing import Optional

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from teleflow_common.database import Base, TimestampMixin


class CRMSegment(Base, TimestampMixin):
    """CRM segment for user targeting."""

    __tablename__ = "crm_segments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Filter conditions
    conditions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # {"operator": "AND", "rules": [{"field": "tag", "op": "in", "value": ["vip"]}, ...]}

    # Stats
    user_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<CRMSegment(id={self.id}, name={self.name})>"
