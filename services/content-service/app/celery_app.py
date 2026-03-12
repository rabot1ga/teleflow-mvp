"""
Celery application for Content Service.
"""

from celery import Celery

from app.config import settings


celery_app = Celery(
    "content_service",
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
        "app.tasks.fetch_source": {"queue": "content"},
        "app.tasks.fetch_all_sources": {"queue": "content"},
        "app.tasks.apply_rules": {"queue": "content"},
        "app.tasks.sync_meilisearch": {"queue": "content"},
    },
)
