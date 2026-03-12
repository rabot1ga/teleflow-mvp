"""
Event consumers for Publishing Service.

Listens for events from other services via Redis Pub/Sub.
"""

import asyncio
import json

import structlog
from redis.asyncio import Redis

from app.celery_app import celery_app
from app.config import settings
from app.database import async_session_factory
from app.models.job import PublishJob
from app.models.target import PublishTarget
from app.services.job_service import PublishJobService
from sqlalchemy import select

logger = structlog.get_logger()


async def handle_article_approved(event: dict):
    """
    Handle article.approved event.

    Creates publish jobs for approved articles.

    Event payload:
    - article_id: str
    - target_id: str (optional, if specified by moderator)
    - schedule_at: str (optional, ISO datetime)
    """
    article_id = event.get("article_id")
    target_id = event.get("target_id")
    schedule_at = event.get("schedule_at")

    if not article_id:
        logger.error("article_approved_missing_article_id", event=event)
        return

    async with async_session_factory() as db:
        # Get default targets for the project
        # In a real scenario, we'd get project_id from article
        # For now, we'll create a job for all active targets
        
        if target_id:
            # Specific target requested
            result = await db.execute(
                select(PublishTarget).where(
                    PublishTarget.id == target_id,
                    PublishTarget.is_active == True
                )
            )
            targets = [result.scalar_one_or_none()]
            targets = [t for t in targets if t is not None]
        else:
            # Get all active targets (default behavior)
            result = await db.execute(
                select(PublishTarget).where(
                    PublishTarget.is_active == True
                )
            )
            targets = result.scalars().all()

        if not targets:
            logger.warning("no_active_targets", article_id=article_id)
            return

        # Create publish jobs
        job_service = PublishJobService(db)
        jobs_created = 0

        for target in targets:
            job_data = {
                "project_id": target.project_id,
                "article_id": article_id,
                "target_id": target.id,
            }
            
            if schedule_at:
                job_data["scheduled_at"] = schedule_at

            try:
                job = await job_service.create_job(type("obj", (object,), job_data))
                jobs_created += 1
                
                # Trigger immediate publish if not scheduled
                if not schedule_at:
                    celery_app.send_task("app.tasks.publish_article", args=[job.id])
                    
            except Exception as e:
                logger.error(
                    "failed_to_create_job",
                    article_id=article_id,
                    target_id=target.id,
                    error=str(e),
                )

        logger.info(
            "article_approved_processed",
            article_id=article_id,
            jobs_created=jobs_created,
        )


async def start_event_listener():
    """Start Redis Pub/Sub event listener."""
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    
    # Subscribe to events
    await pubsub.subscribe("teleflow:article.approved")
    
    logger.info("event_listener_started", channels=["teleflow:article.approved"])
    
    async for message in pubsub.listen():
        try:
            if message["type"] == "message":
                event_type = message["channel"].replace("teleflow:", "")
                event_data = json.loads(message["data"])
                
                logger.info("event_received", event_type=event_type, event_data=event_data)
                
                if event_type == "article.approved":
                    await handle_article_approved(event_data)
                    
        except Exception as e:
            logger.error("event_listener_error", error=str(e))
    
    await pubsub.close()
    await redis.close()


# Export for Celery
@celery_app.task
def start_event_listener_task():
    """Start event listener as Celery task."""
    asyncio.run(start_event_listener())
