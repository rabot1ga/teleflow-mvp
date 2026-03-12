"""
Funnel model - marketing funnels.
"""

import uuid
from typing import Optional

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class Funnel(Base, TimestampMixin):
    """Marketing funnel."""

    __tablename__ = "funnels"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Trigger
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # command, command_with_param, deep_link, button_click, subscription, first_message
    trigger_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Stats
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relationships
    steps: Mapped[list["FunnelStep"]] = relationship(  # noqa: F821
        "FunnelStep",
        back_populates="funnel",
        cascade="all, delete-orphan",
        order_by="FunnelStep.step_order",
    )
    users: Mapped[list["FunnelUser"]] = relationship(  # noqa: F821
        "FunnelUser",
        back_populates="funnel",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Funnel(id={self.id}, name={self.name}, trigger={self.trigger_type})>"
