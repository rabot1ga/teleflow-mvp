"""
Broadcast service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.broadcast import Broadcast
from app.schemas.broadcast import BroadcastCreate, BroadcastUpdate

logger = structlog.get_logger()


class BroadcastService:
    """Broadcast business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_broadcast(self, data: BroadcastCreate) -> Broadcast:
        """Create a new broadcast."""
        broadcast = Broadcast(
            project_id=data.project_id,
            name=data.name,
            message_type=data.message_type,
            message_text=data.message_text,
            message_media_url=data.message_media_url,
            buttons=data.buttons,
            recipient_filter=data.recipient_filter,
            scheduled_at=data.scheduled_at,
            send_rate=data.send_rate,
            status="draft" if not data.scheduled_at else "scheduled",
        )

        self.db.add(broadcast)
        await self.db.flush()

        logger.info(
            "broadcast_created",
            broadcast_id=broadcast.id,
            name=broadcast.name,
        )

        return broadcast

    async def get_by_id(self, broadcast_id: str) -> Optional[Broadcast]:
        """Get broadcast by ID."""
        result = await self.db.execute(
            select(Broadcast).where(Broadcast.id == broadcast_id)
        )
        return result.scalar_one_or_none()

    async def list_broadcasts(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> Tuple[List[Broadcast], int]:
        """List broadcasts with pagination."""
        query = select(Broadcast).where(Broadcast.project_id == project_id)

        if status is not None:
            query = query.where(Broadcast.status == status)

        # Get total count
        count_query = select(Broadcast.id).where(Broadcast.project_id == project_id)
        if status is not None:
            count_query = count_query.where(Broadcast.status == status)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Broadcast.created_at.desc())
        result = await self.db.execute(query)
        broadcasts = result.scalars().all()

        return list(broadcasts), total

    async def update_broadcast(
        self,
        broadcast: Broadcast,
        data: BroadcastUpdate,
    ) -> Broadcast:
        """Update broadcast."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(broadcast, field, value)

        await self.db.flush()

        logger.info(
            "broadcast_updated",
            broadcast_id=broadcast.id,
            fields=list(update_data.keys()),
        )

        return broadcast

    async def delete_broadcast(self, broadcast: Broadcast) -> None:
        """Delete broadcast."""
        await self.db.delete(broadcast)

        logger.info(
            "broadcast_deleted",
            broadcast_id=broadcast.id,
        )

    async def start_broadcast(self, broadcast: Broadcast) -> Broadcast:
        """Start broadcast."""
        broadcast.status = "running"
        broadcast.started_at = None  # Will be set by worker
        await self.db.flush()

        logger.info(
            "broadcast_started",
            broadcast_id=broadcast.id,
        )

        return broadcast

    async def cancel_broadcast(self, broadcast: Broadcast) -> Broadcast:
        """Cancel broadcast."""
        broadcast.status = "cancelled"
        await self.db.flush()

        logger.info(
            "broadcast_cancelled",
            broadcast_id=broadcast.id,
        )

        return broadcast
