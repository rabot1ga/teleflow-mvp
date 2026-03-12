"""
Celery application for Funnel Service.
"""

from celery import Celery

from app.config import settings


celery_app = Celery(
    "funnel_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.tasks.process_funnel_step": {"queue": "funnel"},
        "app.tasks.check_pending_steps": {"queue": "funnel"},
        "app.tasks.execute_broadcast": {"queue": "funnel"},
    },
)
