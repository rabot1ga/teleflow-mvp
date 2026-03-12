"""
Articles API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.article import ArticleList, ArticleResponse, ArticleUpdate
from app.services.article_service import ArticleService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/articles", tags=["Articles"])


def get_article_service(db=Depends(get_async_session)) -> ArticleService:
    """Get article service instance."""
    return ArticleService(db)


@router.get(
    "",
    response_model=StandardResponse[ArticleList],
    summary="List articles",
)
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    category: str | None = None,
    source_id: str | None = None,
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleList]:
    """List articles with pagination and filters."""
    skip = (page - 1) * per_page
    
    # Get project_id from user context (for multi-tenancy)
    # For now, use a default project_id
    project_id = current_user.get("project_id", "test-project")
    
    articles, total = await article_service.list_articles(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        status=status_filter,
        category=category,
        source_id=source_id,
    )

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
    "/{article_id}",
    response_model=StandardResponse[ArticleResponse],
    summary="Get article by ID",
)
async def get_article(
    article_id: str,
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleResponse]:
    """Get article by ID."""
    article = await article_service.get_by_id(article_id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    return StandardResponse(
        data=ArticleResponse.model_validate(article),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{article_id}",
    response_model=StandardResponse[ArticleResponse],
    summary="Update article",
)
async def update_article(
    article_id: str,
    data: ArticleUpdate,
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleResponse]:
    """Update article."""
    article = await article_service.get_by_id(article_id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    updated_article = await article_service.update_article(
        article,
        data,
        changed_by=current_user.get("user_id"),
    )

    return StandardResponse(
        data=ArticleResponse.model_validate(updated_article),
        meta=ResponseMeta(request_id=""),
    )


@router.post(
    "/{article_id}/approve",
    response_model=StandardResponse[ArticleResponse],
    summary="Approve article",
)
async def approve_article(
    article_id: str,
    target_id: str | None = None,
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleResponse]:
    """Approve article for publishing."""
    article = await article_service.get_by_id(article_id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    approved_article = await article_service.approve_article(
        article,
        moderated_by=current_user.get("user_id"),
        target_id=target_id,
    )

    return StandardResponse(
        data=ArticleResponse.model_validate(approved_article),
        meta=ResponseMeta(request_id=""),
    )


@router.post(
    "/{article_id}/reject",
    response_model=StandardResponse[ArticleResponse],
    summary="Reject article",
)
async def reject_article(
    article_id: str,
    reason: str = Query(..., min_length=1),
    comment: str | None = None,
    article_service: ArticleService = Depends(get_article_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[ArticleResponse]:
    """Reject article."""
    article = await article_service.get_by_id(article_id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    rejected_article = await article_service.reject_article(
        article,
        moderated_by=current_user.get("user_id"),
        reason=reason,
        comment=comment,
    )

    return StandardResponse(
        data=ArticleResponse.model_validate(rejected_article),
        meta=ResponseMeta(request_id=""),
    )
