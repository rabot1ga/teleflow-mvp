"""
Standard response schemas for TeleFlow APIs.
"""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


DataT = TypeVar("DataT")


class ResponseMeta(BaseModel):
    """Meta information in response."""

    request_id: str = Field(..., description="Request correlation ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class StandardResponse(BaseModel, Generic[DataT]):
    """
    Standard success response format.
    """

    success: bool = Field(default=True, description="Operation success flag")
    data: DataT = Field(..., description="Response data")
    meta: ResponseMeta = Field(default_factory=lambda: ResponseMeta(request_id="auto-generated"), description="Response metadata")


class ErrorDetail(BaseModel):
    """Detailed error information."""

    field: str = Field(..., description="Field name")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    """

    success: bool = Field(default=False, description="Operation success flag")
    error: dict = Field(..., description="Error details")
    meta: ResponseMeta = Field(..., description="Response metadata")

    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        details: Optional[List[dict]] = None,
        request_id: str = "",
    ) -> "ErrorResponse":
        """Create error response."""
        error_data = {
            "code": code,
            "message": message,
        }
        if details:
            error_data["details"] = details

        return cls(
            error=error_data,
            meta=ResponseMeta(request_id=request_id),
        )


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """
    Paginated response format.
    """

    success: bool = Field(default=True)
    data: List[DataT] = Field(..., description="Items on current page")
    pagination: dict = Field(..., description="Pagination metadata")
    meta: ResponseMeta = Field(..., description="Response metadata")

    @classmethod
    def create(
        cls,
        items: List[DataT],
        total: int,
        page: int,
        per_page: int,
        request_id: str = "",
    ) -> "PaginatedResponse[DataT]":
        """Create paginated response."""
        pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        return cls(
            data=items,
            pagination={
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "has_next": page < pages,
                "has_prev": page > 1,
            },
            meta=ResponseMeta(request_id=request_id),
        )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
