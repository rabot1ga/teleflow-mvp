"""
Article service - business logic for articles.
"""

import hashlib
import json
from datetime import datetime
from typing import List, Optional, Tuple

import structlog
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

logger = structlog.get_logger()


class ArticleService:
    """Article business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _generate_url_hash(self, url: str) -> str:
        """Generate SHA256 hash from URL."""
        return hashlib.sha256(url.encode()).hexdigest()

    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA256 hash from normalized content."""
        # Normalize content (remove extra whitespace)
        normalized = " ".join(content.split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _calculate_quality_score(
        self,
        title: str,
        content: Optional[str],
        has_image: bool,
        source_reputation: float,
    ) -> float:
        """
        Calculate article quality score (0.0 - 1.0).

        Formula:
        quality = (
            text_length_score * 0.3 +
            has_image * 0.2 +
            freshness * 0.2 +
            source_reputation * 0.2 +
            has_proper_title * 0.1
        )
        """
        # Text length score (0-1 based on length)
        text_length = len(content) if content else 0
        text_length_score = min(1.0, text_length / 500)  # 500 chars = max score

        # Image score
        image_score = 1.0 if has_image else 0.0

        # Title score
        title_score = 1.0 if len(title) > 10 else 0.0

        # Calculate final score
        quality = (
            text_length_score * 0.3 +
            image_score * 0.2 +
            source_reputation * 0.2 +
            title_score * 0.1 +
            0.2  # Base freshness score (will be adjusted later)
        )

        return round(min(1.0, max(0.0, quality)), 2)

    def _calculate_priority_score(
        self,
        quality_score: float,
        category_importance: int = 50,
        source_boost: int = 0,
    ) -> int:
        """
        Calculate priority score (0-100).

        Formula:
        priority = quality * 60 + category_importance * 20 + source_boost * 10 + recency * 10
        """
        priority = int(
            quality_score * 60 +
            (category_importance / 100) * 20 +
            (source_boost + 10) * 0.5 +
            10  # Base recency score
        )

        return min(100, max(0, priority))

    async def create_article(self, data: ArticleCreate) -> Tuple[Article, bool]:
        """
        Create article with deduplication.

        Returns:
            tuple[Article, bool]: Article and is_new flag
        """
        # Check for duplicates by URL hash
        url_hash = self._generate_url_hash(data.url) if data.url else None

        if url_hash:
            existing = await self.db.execute(
                select(Article).where(Article.url_hash == url_hash)
            )
            existing_article = existing.scalar_one_or_none()

            if existing_article:
                logger.info(
                    "article_duplicate",
                    url=data.url,
                    existing_id=existing_article.id,
                )
                return existing_article, False

        # Generate content hash if content exists
        content_hash = None
        if data.content:
            content_hash = self._generate_content_hash(data.content)

        # Create article
        article = Article(
            project_id=data.project_id,
            source_id=data.source_id,
            title=data.title,
            content=data.content,
            url=data.url,
            image_url=data.image_url,
            category=data.category,
            tags=data.tags,
            language=data.language,
            author=data.author,
            url_hash=url_hash,
            content_hash=content_hash,
            original_pub_date=data.original_pub_date,
            status="pending",
        )

        self.db.add(article)
        await self.db.flush()

        logger.info(
            "article_created",
            article_id=article.id,
            title=article.title[:50],
            url_hash=url_hash,
        )

        return article, True

    async def get_by_id(self, article_id: str) -> Optional[Article]:
        """Get article by ID."""
        result = await self.db.execute(
            select(Article).where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    async def list_articles(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        category: Optional[str] = None,
        source_id: Optional[str] = None,
    ) -> Tuple[List[Article], int]:
        """
        List articles with pagination and filters.

        Returns:
            tuple[list[Article], int]: Articles and total count
        """
        query = select(Article).where(Article.project_id == project_id)

        if status is not None:
            query = query.where(Article.status == status)

        if category is not None:
            query = query.where(Article.category == category)

        if source_id is not None:
            query = query.where(Article.source_id == source_id)

        # Get total count
        count_query = select(Article.id).where(Article.project_id == project_id)
        if status is not None:
            count_query = count_query.where(Article.status == status)
        if category is not None:
            count_query = count_query.where(Article.category == category)
        if source_id is not None:
            count_query = count_query.where(Article.source_id == source_id)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Article.created_at.desc())
        result = await self.db.execute(query)
        articles = result.scalars().all()

        return list(articles), total

    async def update_article(
        self,
        article: Article,
        data: ArticleUpdate,
        changed_by: Optional[str] = None,
    ) -> Article:
        """Update article and create version."""
        from app.models.article_version import ArticleVersion

        update_data = data.model_dump(exclude_unset=True)
        changes = {}

        for field, value in update_data.items():
            if getattr(article, field) != value:
                changes[field] = {
                    "old": getattr(article, field),
                    "new": value,
                }
                setattr(article, field, value)

        # Create version record if there are changes
        if changes:
            version = ArticleVersion(
                article_id=article.id,
                title=article.title,
                content=article.content,
                changed_by=changed_by,
                change_type="edited",
            )
            self.db.add(version)

        await self.db.flush()

        logger.info(
            "article_updated",
            article_id=article.id,
            changes=list(changes.keys()),
        )

        return article

    async def approve_article(
        self,
        article: Article,
        moderated_by: str,
        target_id: Optional[str] = None,
    ) -> Article:
        """Approve article for publishing."""
        article.status = "approved"
        article.moderated_by = moderated_by
        article.moderated_at = datetime.utcnow()
        article.publish_target_id = target_id

        await self.db.flush()

        # Publish event for publishing-service
        await self._publish_article_approved(article.id, target_id)

        logger.info(
            "article_approved",
            article_id=article.id,
            moderated_by=moderated_by,
        )

        return article

    async def _publish_article_approved(
        self,
        article_id: str,
        target_id: Optional[str] = None,
    ) -> None:
        """Publish article.approved event to Redis Pub/Sub."""
        try:
            redis_url = "redis://redis:6379/0"
            redis = Redis.from_url(redis_url, decode_responses=True)
            
            event_data = {
                "article_id": article_id,
                "target_id": target_id,
            }
            
            await redis.publish("teleflow:article.approved", json.dumps(event_data))
            await redis.close()
            
            logger.info(
                "event_published",
                event_type="article.approved",
                article_id=article_id,
            )
        except Exception as e:
            logger.error("failed_to_publish_event", event_type="article.approved", error=str(e))

    async def reject_article(
        self,
        article: Article,
        moderated_by: str,
        reason: str,
        comment: Optional[str] = None,
    ) -> Article:
        """Reject article."""
        article.status = "rejected"
        article.moderated_by = moderated_by
        article.moderated_at = datetime.utcnow()
        article.rejection_reason = reason
        article.rejection_comment = comment

        await self.db.flush()

        logger.info(
            "article_rejected",
            article_id=article.id,
            reason=reason,
        )

        return article
