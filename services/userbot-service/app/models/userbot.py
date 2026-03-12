"""
Userbot Account models.
"""

import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AccountStatus(str, enum.Enum):
    """Status of userbot account."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    BANNED = "banned"
    NEEDS_AUTH = "needs_auth"
    NEEDS_2FA = "needs_2fa"


class UserbotAccount(Base):
    """Telegram userbot account."""

    __tablename__ = "userbot_accounts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    project_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
    )
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        unique=True,
    )
    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Auth state
    status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus),
        default=AccountStatus.NEEDS_AUTH,
        nullable=False,
    )
    auth_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    auth_code_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    phone_code_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    two_fa_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Session (encrypted)
    session_string: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Warming
    is_warming_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    warming_day: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    warming_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_warming_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Stats
    is_online: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
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

    # Relationships
    proxies: Mapped[list["Proxy"]] = relationship(
        "Proxy",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<UserbotAccount(id={self.id}, username={self.username})>"
