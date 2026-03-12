"""
Celery Beat configuration for TeleFlow Platform.

Scheduled tasks:
- fetch_all_sources: Every 5 minutes
- check_pending_funnel_steps: Every 10 seconds
- check_scheduled_publish_jobs: Every 1 minute
- aggregate_daily_stats: Every 1 hour
"""

from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery_app = Celery("celery_beat", broker=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Scheduled tasks
    beat_schedule={
        # Content Service: Fetch all active sources every 5 minutes
        "fetch-all-sources": {
            "task": "app.tasks.fetch_all_sources",
            "schedule": 300.0,  # 5 minutes
        },
    },
    # Task routing
    task_routes={
        "app.tasks.fetch_all_sources": {"queue": "content"},
    },
)
