"""AI Service schemas."""

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
    UsageStats,
)

__all__ = [
    "RewriteRequest",
    "RewriteResponse",
    "SummarizeRequest",
    "SummarizeResponse",
    "ClassifyRequest",
    "ClassifyResponse",
    "TranslateRequest",
    "TranslateResponse",
    "GenerateTagsRequest",
    "GenerateTagsResponse",
    "ModerateRequest",
    "ModerateResponse",
    "GenerateRequest",
    "GenerateResponse",
    "UsageStats",
]
