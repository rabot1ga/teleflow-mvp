"""
Celery tasks for Publishing Service.
"""

import asyncio
from datetime import datetime

import httpx
import structlog

from app.celery_app import celery_app
from app.database import async_session_factory
from app.models.job import PublishJob
from app.models.target import PublishTarget
from sqlalchemy import select

logger = structlog.get_logger()


@celery_app.task(bind=True, max_retries=3)
def publish_article(self, job_id: str) -> dict:
    """
    Publish article to Telegram channel.

    Steps:
    1. Get job from DB
    2. Get article from content-service
    3. Get template
    4. Render message
    5. Send via bot-gateway
    6. Update job status
    """
    async def _publish():
        async with async_session_factory() as db:
            # Get job
            result = await db.execute(
                select(PublishJob).where(PublishJob.id == job_id)
            )
            job = result.scalar_one_or_none()

            if not job:
                logger.error("publish_job_not_found", job_id=job_id)
                return {"status": "error", "error": "Job not found"}

            # Update status
            job.status = "publishing"
            await db.flush()

            try:
                # Get target
                target_result = await db.execute(
                    select(PublishTarget).where(PublishTarget.id == job.target_id)
                )
                target = target_result.scalar_one_or_none()

                if not target:
                    raise Exception("Target not found")

                # Get article from content-service
                async with httpx.AsyncClient(timeout=30.0) as client:
                    article_resp = await client.get(
                        f"http://content-service:8002/api/v1/content/articles/{job.article_id}"
                    )
                    if article_resp.status_code != 200:
                        raise Exception("Article not found in content-service")
                    
                    article_data = article_resp.json()
                    article = article_data.get("data", {})

                # Render message
                message_text = render_message(article, job.template_id)

                # Send via bot-gateway
                async with httpx.AsyncClient(timeout=30.0) as client:
                    send_resp = await client.post(
                        "http://bot-gateway:8006/internal/bot/send-message",
                        json={
                            "chat_id": target.telegram_chat_id,
                            "text": message_text,
                            "parse_mode": "HTML",
                        }
                    )
                    
                    if send_resp.status_code != 200:
                        raise Exception("Failed to send message")
                    
                    send_data = send_resp.json()
                    message_id = send_data.get("data", {}).get("message_id")

                # Update job
                job.status = "published"
                job.published_at = datetime.utcnow()
                job.telegram_message_id = message_id

                await db.flush()

                logger.info(
                    "article_published",
                    job_id=job.id,
                    article_id=job.article_id,
                    message_id=message_id,
                )

                return {
                    "status": "published",
                    "message_id": message_id,
                }

            except Exception as e:
                job.status = "failed"
                job.error = str(e)
                job.retry_count += 1
                
                if job.retry_count < 3:
                    # Retry in 5 minutes
                    raise self.retry(exc=e, countdown=300)
                
                await db.flush()
                
                logger.error(
                    "publish_failed",
                    job_id=job.id,
                    error=str(e),
                )
                
                return {"status": "failed", "error": str(e)}

    return asyncio.run(_publish())


def render_message(article: dict, template_id: str) -> str:
    """Render message from template."""
    # Default template if no template_id
    title = article.get("title", "Без названия")
    content = article.get("content", "")[:500]  # First 500 chars
    url = article.get("url", "")
    
    # Simple default template
    message = f"<b>{title}</b>\n\n"
    if content:
        message += f"{content}\n\n"
    if url:
        message += f"🔗 <a href=\"{url}\">Читать далее</a>"
    
    return message


@celery_app.task
def check_scheduled_jobs() -> dict:
    """
    Check and publish scheduled jobs.
    
    Triggered by Celery Beat every minute.
    """
    async def _check():
        async with async_session_factory() as db:
            now = datetime.utcnow()
            
            # Get pending jobs that are scheduled
            result = await db.execute(
                select(PublishJob)
                .where(PublishJob.status == "pending")
                .where(PublishJob.scheduled_at <= now)
                .limit(10)
            )
            jobs = result.scalars().all()
            
            logger.info("scheduled_jobs_check", count=len(jobs))
            
            # Trigger publish for each job
            for job in jobs:
                publish_article.delay(job.id)
            
            return {
                "status": "checked",
                "jobs_triggered": len(jobs),
            }
    
    return asyncio.run(_check())
