"""API routers for AI operations in Content Service."""

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/ai", tags=["AI Operations"])

AI_SERVICE_URL = "http://ai-service:8009"


@router.post("/rewrite", response_model=StandardResponse[dict])
async def rewrite_article(
    article_id: str,
    project_id: str,
    style: str = "neutral",
    tone: str = "formal",
    session: AsyncSession = Depends(get_async_session),
):
    """
    Rewrite article content using AI.
    
    This endpoint calls AI Service to rewrite the article content,
    then updates the article with the rewritten version.
    """
    from sqlalchemy import select
    from app.models.article import Article, ArticleVersion
    
    # Get article
    result = await session.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    if not article.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article has no content to rewrite",
        )
    
    # Call AI Service
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{AI_SERVICE_URL}/api/v1/ai/rewrite",
                params={"project_id": project_id},
                json={
                    "text": article.content,
                    "style": style,
                    "tone": tone,
                },
            )
            response.raise_for_status()
            ai_result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI Service error: {str(e)}",
            )
    
    if not ai_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI rewrite failed",
        )
    
    # Save original as version
    version = ArticleVersion(
        article_id=article.id,
        title=article.title,
        content=article.content,
        change_type="ai_rewritten",
    )
    session.add(version)
    
    # Update article with rewritten content
    rewritten_text = ai_result.get("data", {}).get("text", "")
    article.content = rewritten_text
    article.summary = None  # Clear summary to regenerate
    
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={
            "message": "Article rewritten successfully",
            "article_id": article_id,
            "original_length": len(article.content),
            "new_length": len(rewritten_text),
        },
    )


@router.post("/summarize", response_model=StandardResponse[dict])
async def summarize_article(
    article_id: str,
    project_id: str,
    max_length: int = 100,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Generate summary for article using AI.
    """
    from sqlalchemy import select
    from app.models.article import Article
    
    # Get article
    result = await session.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    if not article.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article has no content to summarize",
        )
    
    # Call AI Service
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{AI_SERVICE_URL}/api/v1/ai/summarize",
                params={"project_id": project_id},
                json={
                    "text": article.content,
                    "max_length": max_length,
                },
            )
            response.raise_for_status()
            ai_result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI Service error: {str(e)}",
            )
    
    if not ai_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI summarization failed",
        )
    
    # Update article summary
    summary = ai_result.get("data", {}).get("text", "")
    article.summary = summary
    
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={
            "message": "Summary generated successfully",
            "article_id": article_id,
            "summary_length": len(summary),
        },
    )


@router.post("/classify", response_model=StandardResponse[dict])
async def classify_article(
    article_id: str,
    project_id: str,
    categories: list[str] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Classify article into category using AI.
    """
    from sqlalchemy import select
    from app.models.article import Article
    
    # Default categories
    if categories is None:
        categories = [
            "technology",
            "business",
            "science",
            "politics",
            "sports",
            "entertainment",
            "health",
            "other",
        ]
    
    # Get article
    result = await session.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    text_to_classify = f"{article.title}\n\n{article.content or ''}"
    
    # Call AI Service
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{AI_SERVICE_URL}/api/v1/ai/classify",
                params={"project_id": project_id},
                json={
                    "text": text_to_classify,
                    "categories": categories,
                },
            )
            response.raise_for_status()
            ai_result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI Service error: {str(e)}",
            )
    
    if not ai_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI classification failed",
        )
    
    # Update article category
    predicted_category = ai_result.get("data", {}).get("category", "")
    article.category = predicted_category
    
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={
            "message": "Article classified successfully",
            "article_id": article_id,
            "category": predicted_category,
            "confidence": ai_result.get("data", {}).get("confidence", 0),
        },
    )


@router.post("/generate-tags", response_model=StandardResponse[dict])
async def generate_article_tags(
    article_id: str,
    project_id: str,
    max_tags: int = 10,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Generate tags for article using AI.
    """
    from sqlalchemy import select
    from app.models.article import Article
    
    # Get article
    result = await session.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    text_to_analyze = f"{article.title}\n\n{article.content or ''}"
    
    # Call AI Service (using generate endpoint when implemented)
    # For now, use classify with tag-like categories
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Simple tag generation using prompt
            response = await client.post(
                f"{AI_SERVICE_URL}/api/v1/ai/generate",
                params={"project_id": project_id},
                json={
                    "prompt": f"Generate {max_tags} relevant tags for this content (comma-separated):\n\n{text_to_analyze}",
                    "max_tokens": 100,
                    "temperature": 0.5,
                },
            )
            response.raise_for_status()
            ai_result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI Service error: {str(e)}",
            )
    
    if not ai_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI tag generation failed",
        )
    
    # Parse tags from response
    generated_text = ai_result.get("data", {}).get("text", "")
    tags = [tag.strip() for tag in generated_text.split(",") if tag.strip()]
    article.tags = tags[:max_tags]
    
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={
            "message": "Tags generated successfully",
            "article_id": article_id,
            "tags": tags[:max_tags],
        },
    )
