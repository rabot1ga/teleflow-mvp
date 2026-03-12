"""
Database module for TeleFlow services.
"""

from datetime import datetime
from typing import Any, AsyncGenerator, Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at columns.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class SoftDeleteMixin:
    """
    Mixin that adds soft delete functionality.
    """

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


def create_async_engine_instance(
    database_url: str,
    echo: bool = False,
    pool_pre_ping: bool = True,
) -> Any:
    """
    Create async SQLAlchemy engine.

    Args:
        database_url: PostgreSQL connection URL
        echo: Enable SQL echo
        pool_pre_ping: Enable connection health checks

    Returns:
        AsyncEngine instance
    """
    return create_async_engine(
        database_url,
        echo=echo,
        pool_pre_ping=pool_pre_ping,
        poolclass=NullPool,
    )


def create_async_session_factory(
    engine: Any,
) -> async_sessionmaker[AsyncSession]:
    """
    Create async session factory.

    Args:
        engine: AsyncEngine instance

    Returns:
        AsyncSession factory
    """
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.

    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
