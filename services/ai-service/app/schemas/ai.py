"""Pydantic schemas for AI API."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ==================== Request Schemas ====================


class RewriteRequest(BaseModel):
    """Request for text rewrite."""

    text: str = Field(..., min_length=1, max_length=50000)
    style: str = Field(default="neutral", description="Writing style")
    tone: str = Field(default="formal", description="Text tone")
    provider: Optional[str] = Field(None, description="AI provider (openai, anthropic, ollama)")


class SummarizeRequest(BaseModel):
    """Request for text summarization."""

    text: str = Field(..., min_length=1, max_length=100000)
    max_length: int = Field(default=100, ge=10, le=1000)
    provider: Optional[str] = Field(None, description="AI provider")


class ClassifyRequest(BaseModel):
    """Request for text classification."""

    text: str = Field(..., min_length=1, max_length=50000)
    categories: List[str] = Field(..., min_length=2, description="Categories to classify into")
    provider: Optional[str] = Field(None, description="AI provider")


class TranslateRequest(BaseModel):
    """Request for text translation."""

    text: str = Field(..., min_length=1, max_length=50000)
    source_language: str = Field(default="auto", description="Source language code")
    target_language: str = Field(..., description="Target language code")
    provider: Optional[str] = Field(None, description="AI provider")


class GenerateTagsRequest(BaseModel):
    """Request for tag generation."""

    text: str = Field(..., min_length=1, max_length=50000)
    max_tags: int = Field(default=10, ge=1, le=50)
    provider: Optional[str] = Field(None, description="AI provider")


class ModerateRequest(BaseModel):
    """Request for content moderation."""

    text: str = Field(..., min_length=1, max_length=50000)
    provider: Optional[str] = Field(None, description="AI provider")


class GenerateRequest(BaseModel):
    """Generic generation request."""

    prompt: str = Field(..., min_length=1, max_length=10000)
    system_prompt: Optional[str] = Field(None, description="System prompt")
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1024, ge=1, le=8192)
    provider: Optional[str] = Field(None, description="AI provider")


# ==================== Response Schemas ====================


class AIResponse(BaseModel):
    """Generic AI response."""

    text: str
    is_cached: bool = False
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


class RewriteResponse(AIResponse):
    """Response for rewrite operation."""

    style: str
    tone: str


class SummarizeResponse(AIResponse):
    """Response for summarize operation."""

    original_length: int
    summary_length: int
    compression_ratio: float


class ClassifyResponse(BaseModel):
    """Response for classification operation."""

    category: str
    confidence: float
    all_categories: List[str]
    is_cached: bool = False


class TranslateResponse(AIResponse):
    """Response for translation operation."""

    source_language: str
    target_language: str


class GenerateTagsResponse(BaseModel):
    """Response for tag generation."""

    tags: List[str]
    is_cached: bool = False


class ModerateResponse(BaseModel):
    """Response for moderation operation."""

    is_safe: bool
    categories: Dict[str, float]  # category -> confidence
    explanation: Optional[str] = None
    is_cached: bool = False


class GenerateResponse(AIResponse):
    """Response for generic generation."""

    pass


class UsageStats(BaseModel):
    """AI usage statistics."""

    total_requests: int
    successful_requests: int
    failed_requests: int
    cached_requests: int
    total_input_tokens: int
    total_output_tokens: int
    avg_latency_ms: Optional[int] = None
