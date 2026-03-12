"""
PublishTemplate model - templates for published articles.
"""

import uuid
from typing import Optional

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from teleflow_common.database import Base, TimestampMixin


class PublishTemplate(Base, TimestampMixin):
    """Publish template for articles."""

    __tablename__ = "publish_templates"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Template
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # Example: "{emoji} <b>{title}</b>\n\n{content_short}\n\n🔗 {read_more}\n\n{tags_hashtags}"

    # Settings
    parse_mode: Mapped[str] = mapped_column(String(10), default="HTML", nullable=False)
    disable_preview: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Buttons (inline keyboard)
    buttons: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    # [{"text": "Читать", "url": "{url}"}, {"text": "👍", "callback_data": "like_{id}"}]

    # Scope
    scope: Mapped[str] = mapped_column(String(20), default="global", nullable=False)
    # global, target, category, source
    scope_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<PublishTemplate(id={self.id}, name={self.name})>"
