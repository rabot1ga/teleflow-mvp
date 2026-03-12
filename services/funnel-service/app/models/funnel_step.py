"""
FunnelStep model - steps in a funnel.
"""

import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from teleflow_common.database import Base, TimestampMixin


class FunnelStep(Base, TimestampMixin):
    """Step in a marketing funnel."""

    __tablename__ = "funnel_steps"

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
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Delay
    delay_type: Mapped[str] = mapped_column(String(20), default="immediate", nullable=False)
    # immediate, seconds, minutes, hours, days, specific_time, next_day_at
    delay_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    delay_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Condition (optional)
    condition: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Actions
    actions: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # On failure
    on_condition_fail: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    funnel: Mapped["Funnel"] = relationship(  # noqa: F821
        "Funnel",
        back_populates="steps",
    )

    def __repr__(self) -> str:
        return f"<FunnelStep(id={self.id}, funnel_id={self.funnel_id}, order={self.step_order})>"
