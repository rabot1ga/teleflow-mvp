"""
Session data models.
"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SessionData(Base):
    """Encrypted session data for Telethon."""

    __tablename__ = "session_data"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        unique=True,
    )

    # Encrypted session data
    # Contains: dc_id, server, port, auth_key, user session
    encrypted_session: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Session metadata
    dc_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    server: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    port: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Status
    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<SessionData(id={self.id}, account_id={self.account_id})>"
