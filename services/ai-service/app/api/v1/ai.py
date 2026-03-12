"""API v1 routers for AI Service."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.schemas.ai import (
    ClassifyRequest,
    ClassifyResponse,
    GenerateRequest,
    GenerateResponse,
    GenerateTagsRequest,
    GenerateTagsResponse,
    ModerateRequest,
    ModerateResponse,
    RewriteRequest,
    RewriteResponse,
    SummarizeRequest,
    SummarizeResponse,
    TranslateRequest,
    TranslateResponse,
)
from app.services.ai_service import AIService
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/ai", tags=["AI Operations"])


def get_ai_service() -> AIService:
    """Get AI service instance."""
    import os
    
    return AIService(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434"),
        redis_url=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    )


@router.post("/rewrite", response_model=StandardResponse[RewriteResponse])
async def rewrite_text(
    request: RewriteRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[RewriteResponse]:
    """Rewrite text in different style."""
    try:
        result = await ai_service.rewrite(
            text=request.text,
            project_id=project_id,
            session=session,
            style=request.style,
            tone=request.tone,
            provider=request.provider,
        )
        
        return StandardResponse[RewriteResponse](
            success=True,
            data=RewriteResponse(
                text=result["text"],
                is_cached=result.get("is_cached", False),
                model=result.get("model"),
                input_tokens=result.get("input_tokens"),
                output_tokens=result.get("output_tokens"),
                style=request.style,
                tone=request.tone,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize", response_model=StandardResponse[SummarizeResponse])
async def summarize_text(
    request: SummarizeRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[SummarizeResponse]:
    """Summarize text."""
    try:
        result = await ai_service.summarize(
            text=request.text,
            project_id=project_id,
            session=session,
            max_length=request.max_length,
            provider=request.provider,
        )
        
        original_length = len(request.text.split())
        summary_length = len(result["text"].split())
        
        return StandardResponse[SummarizeResponse](
            success=True,
            data=SummarizeResponse(
                text=result["text"],
                is_cached=result.get("is_cached", False),
                model=result.get("model"),
                input_tokens=result.get("input_tokens"),
                output_tokens=result.get("output_tokens"),
                original_length=original_length,
                summary_length=summary_length,
                compression_ratio=summary_length / original_length if original_length > 0 else 0,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify", response_model=StandardResponse[ClassifyResponse])
async def classify_text(
    request: ClassifyRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[ClassifyResponse]:
    """Classify text into categories."""
    try:
        result = await ai_service.classify(
            text=request.text,
            categories=request.categories,
            project_id=project_id,
            session=session,
            provider=request.provider,
        )
        
        return StandardResponse[ClassifyResponse](
            success=True,
            data=ClassifyResponse(
                category=result["category"],
                confidence=result.get("confidence", 0),
                all_categories=request.categories,
                is_cached=result.get("is_cached", False),
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=StandardResponse[TranslateResponse])
async def translate_text(
    request: TranslateRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[TranslateResponse]:
    """Translate text."""
    # TODO: Implement translation
    raise HTTPException(status_code=501, detail="Translation not implemented yet")


@router.post("/generate-tags", response_model=StandardResponse[GenerateTagsResponse])
async def generate_tags(
    request: GenerateTagsRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[GenerateTagsResponse]:
    """Generate tags for text."""
    # TODO: Implement tag generation
    raise HTTPException(status_code=501, detail="Tag generation not implemented yet")


@router.post("/moderate", response_model=StandardResponse[ModerateResponse])
async def moderate_content(
    request: ModerateRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[ModerateResponse]:
    """Moderate content."""
    # TODO: Implement moderation
    raise HTTPException(status_code=501, detail="Moderation not implemented yet")


@router.post("/generate", response_model=StandardResponse[GenerateResponse])
async def generate_text(
    request: GenerateRequest,
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
    ai_service: AIService = Depends(get_ai_service),
) -> StandardResponse[GenerateResponse]:
    """Generic text generation."""
    # TODO: Implement generic generation
    raise HTTPException(status_code=501, detail="Generic generation not implemented yet")
