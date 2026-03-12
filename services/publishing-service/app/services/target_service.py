"""
PublishTarget service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.target import PublishTarget
from app.schemas.target import PublishTargetCreate, PublishTargetUpdate

logger = structlog.get_logger()


class PublishTargetService:
    """PublishTarget business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_target(self, data: PublishTargetCreate) -> PublishTarget:
        """Create a new publish target."""
        target = PublishTarget(
            project_id=data.project_id,
            name=data.name,
            telegram_chat_id=data.telegram_chat_id,
            is_default=data.is_default,
            min_interval_seconds=data.min_interval_seconds,
            max_per_hour=data.max_per_hour,
            max_per_day=data.max_per_day,
            timezone=data.timezone,
            categories=data.categories,
            is_active=data.is_active,
        )

        self.db.add(target)
        await self.db.flush()

        logger.info(
            "publish_target_created",
            target_id=target.id,
            name=target.name,
        )

        return target

    async def get_by_id(self, target_id: str) -> Optional[PublishTarget]:
        """Get target by ID."""
        result = await self.db.execute(
            select(PublishTarget).where(PublishTarget.id == target_id)
        )
        return result.scalar_one_or_none()

    async def list_targets(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[PublishTarget], int]:
        """List targets with pagination."""
        query = select(PublishTarget).where(PublishTarget.project_id == project_id)

        if is_active is not None:
            query = query.where(PublishTarget.is_active == is_active)

        # Get total count
        count_query = select(PublishTarget.id).where(PublishTarget.project_id == project_id)
        if is_active is not None:
            count_query = count_query.where(PublishTarget.is_active == is_active)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(PublishTarget.created_at.desc())
        result = await self.db.execute(query)
        targets = result.scalars().all()

        return list(targets), total

    async def update_target(
        self,
        target: PublishTarget,
        data: PublishTargetUpdate,
    ) -> PublishTarget:
        """Update target."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(target, field, value)

        await self.db.flush()

        logger.info(
            "publish_target_updated",
            target_id=target.id,
            fields=list(update_data.keys()),
        )

        return target

    async def delete_target(self, target: PublishTarget) -> None:
        """Delete target."""
        await self.db.delete(target)

        logger.info(
            "publish_target_deleted",
            target_id=target.id,
        )
