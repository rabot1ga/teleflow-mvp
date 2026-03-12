"""
LeadMagnet service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead_magnet import LeadMagnet
from app.schemas.lead_magnet import LeadMagnetCreate, LeadMagnetUpdate

logger = structlog.get_logger()


class LeadMagnetService:
    """LeadMagnet business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_lead_magnet(self, data: LeadMagnetCreate) -> LeadMagnet:
        """Create a new lead magnet."""
        magnet = LeadMagnet(
            project_id=data.project_id,
            name=data.name,
            type=data.type,
            description=data.description,
            file_id=data.file_id,
            file_path=data.file_path,
            url=data.url,
            text_content=data.text_content,
            delivery_message=data.delivery_message,
            require_subscription=data.require_subscription,
            subscription_channel_id=data.subscription_channel_id,
        )

        self.db.add(magnet)
        await self.db.flush()

        logger.info(
            "lead_magnet_created",
            magnet_id=magnet.id,
            name=magnet.name,
        )

        return magnet

    async def get_by_id(self, magnet_id: str) -> Optional[LeadMagnet]:
        """Get lead magnet by ID."""
        result = await self.db.execute(
            select(LeadMagnet).where(LeadMagnet.id == magnet_id)
        )
        return result.scalar_one_or_none()

    async def list_lead_magnets(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[LeadMagnet], int]:
        """List lead magnets with pagination."""
        query = select(LeadMagnet).where(LeadMagnet.project_id == project_id)

        # Get total count
        count_query = select(LeadMagnet.id).where(LeadMagnet.project_id == project_id)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(LeadMagnet.created_at.desc())
        result = await self.db.execute(query)
        magnets = result.scalars().all()

        return list(magnets), total

    async def update_lead_magnet(
        self,
        magnet: LeadMagnet,
        data: LeadMagnetUpdate,
    ) -> LeadMagnet:
        """Update lead magnet."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(magnet, field, value)

        await self.db.flush()

        logger.info(
            "lead_magnet_updated",
            magnet_id=magnet.id,
            fields=list(update_data.keys()),
        )

        return magnet

    async def delete_lead_magnet(self, magnet: LeadMagnet) -> None:
        """Delete lead magnet."""
        await self.db.delete(magnet)

        logger.info(
            "lead_magnet_deleted",
            magnet_id=magnet.id,
        )
