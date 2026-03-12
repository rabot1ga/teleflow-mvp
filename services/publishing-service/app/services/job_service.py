"""
PublishJob service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import PublishJob
from app.schemas.job import PublishJobCreate, PublishJobUpdate

logger = structlog.get_logger()


class PublishJobService:
    """PublishJob business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, data: PublishJobCreate) -> PublishJob:
        """Create a new publish job."""
        job = PublishJob(
            project_id=data.project_id,
            article_id=data.article_id,
            target_id=data.target_id,
            template_id=data.template_id,
            scheduled_at=data.scheduled_at,
            status="pending",
        )

        self.db.add(job)
        await self.db.flush()

        logger.info(
            "publish_job_created",
            job_id=job.id,
            article_id=job.article_id,
            target_id=job.target_id,
        )

        return job

    async def get_by_id(self, job_id: str) -> Optional[PublishJob]:
        """Get job by ID."""
        result = await self.db.execute(
            select(PublishJob).where(PublishJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        article_id: Optional[str] = None,
    ) -> Tuple[List[PublishJob], int]:
        """List jobs with pagination and filters."""
        query = select(PublishJob).where(PublishJob.project_id == project_id)

        if status is not None:
            query = query.where(PublishJob.status == status)

        if article_id is not None:
            query = query.where(PublishJob.article_id == article_id)

        # Get total count
        count_query = select(PublishJob.id).where(PublishJob.project_id == project_id)
        if status is not None:
            count_query = count_query.where(PublishJob.status == status)
        if article_id is not None:
            count_query = count_query.where(PublishJob.article_id == article_id)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(PublishJob.created_at.desc())
        result = await self.db.execute(query)
        jobs = result.scalars().all()

        return list(jobs), total

    async def update_job(
        self,
        job: PublishJob,
        data: PublishJobUpdate,
    ) -> PublishJob:
        """Update job."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(job, field, value)

        await self.db.flush()

        logger.info(
            "publish_job_updated",
            job_id=job.id,
            fields=list(update_data.keys()),
        )

        return job

    async def delete_job(self, job: PublishJob) -> None:
        """Delete job."""
        await self.db.delete(job)

        logger.info(
            "publish_job_deleted",
            job_id=job.id,
        )
