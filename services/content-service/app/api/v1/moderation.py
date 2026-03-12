"""
Moderation API endpoints.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select

from app.dependencies import get_async_session
from app.models.article import Article
from app.models.moderation import ModerationBatch
from app.schemas.article import ArticleList, ArticleResponse
from app.services.article_service import ArticleService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse


def get_article_service(db=Depends(get_async_session)) -> ArticleService:
    """Get article service instance."""
    return ArticleService(db)


router = APIRouter(prefix="/moderation", tags=["Moderation"])


@router.get(
    "/queue",
    response_model=StandardResponse[ArticleList],
    summary="Get moderation queue",
)
async def get_moderation_queue(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query("pending", alias="status"),
    category: Optional[str] = None,
    source_id: Optional[str] = None,
    sort: str = Query("-priority_score"),  # -priority_score, created_at, -created_at
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleList]:
    """Get articles pending moderation."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    articles, total = await article_service.list_articles(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        status=status_filter,
        category=category,
        source_id=source_id,
    )
    
    # Sort articles
    if sort.startswith("-"):
        articles.sort(key=lambda a: getattr(a, sort[1:], ""), reverse=True)
    else:
        articles.sort(key=lambda a: getattr(a, sort, ""))

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=ArticleList(
            items=[ArticleResponse.model_validate(a) for a in articles],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/stats",
    response_model=StandardResponse[dict],
    summary="Get moderation stats",
)
async def get_moderation_stats(
    db=Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[dict]:
    """Get moderation queue statistics."""
    project_id = current_user.get("project_id", "test-project")
    
    # Get counts by status
    result = await db.execute(
        select(
            Article.status,
            func.count(Article.id)
        )
        .where(Article.project_id == project_id)
        .group_by(Article.status)
    )
    status_counts = dict(result.all())
    
    # Get pending count
    pending_count = status_counts.get("pending", 0)
    
    # Get avg wait time (simplified)
    avg_wait_minutes = 0  # TODO: Calculate from created_at
    
    return StandardResponse(
        data={
            "pending": pending_count,
            "approved": status_counts.get("approved", 0),
            "rejected": status_counts.get("rejected", 0),
            "published": status_counts.get("published", 0),
            "avg_wait_minutes": avg_wait_minutes,
        },
        meta=ResponseMeta(request_id=""),
    )


@router.post(
    "/batches",
    response_model=StandardResponse[dict],
    summary="Create moderation batch",
)
async def create_moderation_batch(
    article_ids: list[str],
    strategy: str = "by_priority",
    db=Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[dict]:
    """Create a batch of articles for moderation."""
    project_id = current_user.get("project_id", "test-project")
    
    batch = ModerationBatch(
        project_id=project_id,
        moderator_id=current_user.get("user_id"),
        strategy=strategy,
        article_ids=article_ids,
        status="pending",
    )
    
    db.add(batch)
    await db.commit()
    await db.refresh(batch)
    
    return StandardResponse(
        data={
            "batch_id": batch.id,
            "article_count": len(batch.article_ids),
            "strategy": batch.strategy,
        },
        meta=ResponseMeta(request_id=""),
    )
