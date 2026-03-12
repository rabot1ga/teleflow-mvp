"""
Funnel service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.funnel import Funnel
from app.schemas.funnel import FunnelCreate, FunnelUpdate

logger = structlog.get_logger()


class FunnelService:
    """Funnel business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_funnel(self, data: FunnelCreate) -> Funnel:
        """Create a new funnel."""
        funnel = Funnel(
            project_id=data.project_id,
            name=data.name,
            description=data.description,
            trigger_type=data.trigger_type,
            trigger_value=data.trigger_value,
            is_active=data.is_active,
        )

        self.db.add(funnel)
        await self.db.flush()

        logger.info(
            "funnel_created",
            funnel_id=funnel.id,
            name=funnel.name,
        )

        return funnel

    async def get_by_id(self, funnel_id: str) -> Optional[Funnel]:
        """Get funnel by ID."""
        result = await self.db.execute(
            select(Funnel).where(Funnel.id == funnel_id)
        )
        return result.scalar_one_or_none()

    async def list_funnels(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[Funnel], int]:
        """List funnels with pagination."""
        query = select(Funnel).where(Funnel.project_id == project_id)

        if is_active is not None:
            query = query.where(Funnel.is_active == is_active)

        # Get total count
        count_query = select(Funnel.id).where(Funnel.project_id == project_id)
        if is_active is not None:
            count_query = count_query.where(Funnel.is_active == is_active)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Funnel.created_at.desc())
        result = await self.db.execute(query)
        funnels = result.scalars().all()

        return list(funnels), total

    async def update_funnel(
        self,
        funnel: Funnel,
        data: FunnelUpdate,
    ) -> Funnel:
        """Update funnel."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(funnel, field, value)

        await self.db.flush()

        logger.info(
            "funnel_updated",
            funnel_id=funnel.id,
            fields=list(update_data.keys()),
        )

        return funnel

    async def delete_funnel(self, funnel: Funnel) -> None:
        """Delete funnel."""
        await self.db.delete(funnel)

        logger.info(
            "funnel_deleted",
            funnel_id=funnel.id,
        )
