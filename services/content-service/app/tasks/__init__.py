"""
Celery tasks for Content Service.
"""

import feedparser
import httpx
import structlog
from bs4 import BeautifulSoup
from sqlalchemy import select

from app.celery_app import celery_app
from app.database import async_session_factory
from app.models.source import Source
from app.models.source_run import SourceRun
from app.services.article_service import ArticleService
from app.schemas.article import ArticleCreate

logger = structlog.get_logger()


@celery_app.task(bind=True, max_retries=3)
def fetch_source(self, source_id: str) -> dict:
    """
    Fetch articles from a single source.

    Steps:
    1. Fetch source data
    2. Parse entries
    3. Create SourceRun record
    4. Process each entry (dedup, enrich, save)
    5. Update source stats
    """
    import asyncio
    from datetime import datetime

    async def _fetch():
        async with async_session_factory() as db:
            # Get source
            result = await db.execute(
                select(Source).where(Source.id == source_id)
            )
            source = result.scalar_one_or_none()

            if not source:
                logger.error("source_not_found", source_id=source_id)
                return {"status": "error", "error": "Source not found"}

            # Create run record
            run = SourceRun(
                source_id=source_id,
                status="running",
                started_at=datetime.utcnow(),
            )
            db.add(run)
            await db.flush()

            articles_found = 0
            articles_new = 0
            articles_duplicate = 0
            error = None

            try:
                if source.source_type == "rss":
                    # Fetch RSS feed
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.get(source.url)
                        response.raise_for_status()
                        feed_data = response.text

                    # Parse RSS
                    feed = feedparser.parse(feed_data)

                    for entry in feed.entries:
                        articles_found += 1

                        # Extract data
                        title = entry.get("title", "")
                        content = entry.get("description", "")
                        url = entry.get("link", "")

                        # Get image if available
                        image_url = None
                        if "media_content" in entry:
                            for media in entry.media_content:
                                if media.get("type", "").startswith("image/"):
                                    image_url = media.get("url")
                                    break

                        # Create article
                        article_data = ArticleCreate(
                            project_id=source.project_id,
                            source_id=source.id,
                            title=title,
                            content=content[:10000] if content else None,  # Limit content
                            url=url,
                            image_url=image_url,
                            category=source.default_category,
                            tags=source.default_tags,
                            language="ru",
                        )

                        article_service = ArticleService(db)
                        article, is_new = await article_service.create_article(article_data)

                        if is_new:
                            articles_new += 1
                        else:
                            articles_duplicate += 1

                # Update run record
                run.status = "completed"
                run.completed_at = datetime.utcnow()
                run.articles_found = articles_found
                run.articles_new = articles_new
                run.articles_duplicate = articles_duplicate

                # Update source
                source.last_fetch_at = datetime.utcnow()
                source.error_count = 0

                await db.commit()

                logger.info(
                    "source_fetch_completed",
                    source_id=source_id,
                    found=articles_found,
                    new=articles_new,
                    duplicate=articles_duplicate,
                )

                return {
                    "status": "completed",
                    "articles_found": articles_found,
                    "articles_new": articles_new,
                    "articles_duplicate": articles_duplicate,
                }

            except Exception as e:
                run.status = "failed"
                run.completed_at = datetime.utcnow()
                run.error = str(e)

                source.last_error = str(e)
                source.error_count += 1

                await db.commit()

                logger.error(
                    "source_fetch_failed",
                    source_id=source_id,
                    error=str(e),
                )

                # Retry task
                raise self.retry(exc=e, countdown=60)

    return asyncio.run(_fetch())


@celery_app.task
def fetch_all_sources() -> dict:
    """
    Fetch all active sources that are due.

    Triggered by Celery Beat every 5 minutes.
    """
    import asyncio
    from datetime import datetime, timedelta

    async def _fetch():
        async with async_session_factory() as db:
            now = datetime.utcnow()

            # Get due sources
            result = await db.execute(
                select(Source)
                .where(Source.is_active == True)
                .where(
                    (Source.last_fetch_at.is_(None)) |
                    (Source.last_fetch_at != None)  # noqa: E711
                )
                .limit(10)  # Process max 10 sources at once
            )
            sources = result.scalars().all()

            # Filter in Python for simplicity
            due_sources = []
            for source in sources:
                if source.last_fetch_at is None:
                    due_sources.append(source)
                else:
                    next_fetch = source.last_fetch_at + timedelta(minutes=source.fetch_interval_minutes)
                    if next_fetch <= now:
                        due_sources.append(source)

            logger.info("fetch_all_sources", count=len(due_sources))

            # Trigger fetch for each source
            for source in due_sources:
                fetch_source.delay(source.id)

            return {
                "status": "scheduled",
                "sources_count": len(due_sources),
            }

    return asyncio.run(_fetch())


@celery_app.task(bind=True)
def apply_rules(self, article_id: str) -> dict:
    """
    Apply automation rules to an article.

    Rules can:
    - Auto-approve based on quality/source
    - Auto-reject based on keywords
    - Set priority
    - Add tags
    """
    import asyncio

    async def _apply():
        async with async_session_factory() as db:
            # TODO: Implement rules engine
            # For now, just log
            logger.info("apply_rules", article_id=article_id)
            return {"status": "not_implemented"}

    return asyncio.run(_apply())


@celery_app.task(bind=True)
def sync_meilisearch(self, article_id: str) -> dict:
    """
    Sync article to Meilisearch index.
    """
    import asyncio

    async def _sync():
        async with async_session_factory() as db:
            # TODO: Implement Meilisearch sync
            logger.info("sync_meilisearch", article_id=article_id)
            return {"status": "not_implemented"}

    return asyncio.run(_sync())
