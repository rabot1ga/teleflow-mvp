"""
Celery application for Publishing Service.
"""

from celery import Celery
from celery.signals import worker_ready

from app.config import settings


celery_app = Celery(
    "publishing_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks", "app.events"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.tasks.publish_article": {"queue": "publishing"},
        "app.tasks.check_scheduled_jobs": {"queue": "publishing"},
    },
)


@worker_ready.connect
def start_event_listener_on_worker_ready(sender, **kwargs):
    """Start event listener when worker is ready."""
    import asyncio
    from app.events import start_event_listener
    
    # Start in background
    asyncio.create_task(start_event_listener())
    sender.log.info("Event listener started")
