"""
Source service - business logic for content sources.
"""

import hashlib
from datetime import datetime
from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate

logger = structlog.get_logger()


class SourceService:
    """Source business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_source(self, data: SourceCreate) -> Source:
        """Create a new source."""
        source = Source(
            project_id=data.project_id,
            name=data.name,
            source_type=data.source_type,
            url=data.url,
            config=data.config,
            fetch_interval_minutes=data.fetch_interval_minutes,
            default_category=data.default_category,
            default_tags=data.default_tags,
            priority_boost=data.priority_boost,
            reputation=data.reputation,
            is_active=data.is_active,
        )

        self.db.add(source)
        await self.db.flush()

        logger.info(
            "source_created",
            source_id=source.id,
            name=source.name,
            type=source.source_type,
        )

        return source

    async def get_by_id(self, source_id: str) -> Optional[Source]:
        """Get source by ID."""
        result = await self.db.execute(
            select(Source).where(Source.id == source_id)
        )
        return result.scalar_one_or_none()

    async def list_sources(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
        source_type: Optional[str] = None,
    ) -> Tuple[List[Source], int]:
        """
        List sources with pagination.

        Returns:
            tuple[list[Source], int]: Sources and total count
        """
        query = select(Source).where(Source.project_id == project_id)

        if is_active is not None:
            query = query.where(Source.is_active == is_active)

        if source_type is not None:
            query = query.where(Source.source_type == source_type)

        # Get total count
        count_query = select(Source.id).where(Source.project_id == project_id)
        if is_active is not None:
            count_query = count_query.where(Source.is_active == is_active)
        if source_type is not None:
            count_query = count_query.where(Source.source_type == source_type)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Source.created_at.desc())
        result = await self.db.execute(query)
        sources = result.scalars().all()

        return list(sources), total

    async def update_source(
        self,
        source: Source,
        data: SourceUpdate,
    ) -> Source:
        """Update source."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(source, field, value)

        await self.db.flush()

        logger.info(
            "source_updated",
            source_id=source.id,
            fields=list(update_data.keys()),
        )

        return source

    async def delete_source(self, source: Source) -> None:
        """Delete source."""
        await self.db.delete(source)

        logger.info(
            "source_deleted",
            source_id=source.id,
        )

    async def mark_fetched(
        self,
        source: Source,
        error: Optional[str] = None,
    ) -> Source:
        """Mark source as fetched."""
        source.last_fetch_at = datetime.utcnow()

        if error:
            source.last_error = error
            source.error_count += 1
        else:
            source.error_count = 0
            source.last_error = None

        await self.db.flush()

        return source

    async def get_due_sources(self, limit: int = 10) -> List[Source]:
        """Get sources that are due for fetching."""
        from sqlalchemy import func

        now = datetime.utcnow()

        query = (
            select(Source)
            .where(Source.is_active == True)
            .where(
                (Source.last_fetch_at.is_(None)) |
                (
                    Source.last_fetch_at + func.make_interval(
                        mins=Source.fetch_interval_minutes
                    ) <= now
                )
            )
            .order_by(Source.last_fetch_at.asc().nullsfirst())
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())
