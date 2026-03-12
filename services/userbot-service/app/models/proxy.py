"""
Proxy models for userbot accounts.
"""

import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProxyType(str, enum.Enum):
    """Type of proxy."""

    MTProto = "mtproto"
    SOCKS5 = "socks5"
    HTTP = "http"


class Proxy(Base):
    """Proxy server for userbot account."""

    __tablename__ = "proxies"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("userbot_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Proxy details
    proxy_type: Mapped[ProxyType] = mapped_column(
        Enum(ProxyType),
        nullable=False,
    )
    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    port: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    # For MTProto secret
    secret: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    is_working: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )
    last_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    response_time_ms: Mapped[int | None] = mapped_column(
        Integer,
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
    account: Mapped["UserbotAccount"] = relationship(
        "UserbotAccount",
        back_populates="proxies",
    )

    def __repr__(self) -> str:
        return f"<Proxy(id={self.id}, hostname={self.hostname}:{self.port})>"
