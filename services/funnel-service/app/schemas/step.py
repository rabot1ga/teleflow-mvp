"""
FunnelStep schemas.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FunnelStepBase(BaseModel):
    """Base step schema."""

    step_order: int = Field(..., ge=0)
    name: Optional[str] = None
    delay_type: str = "immediate"
    delay_value: Optional[int] = None
    actions: Dict[str, Any] = Field(default_factory=dict)


class FunnelStepCreate(FunnelStepBase):
    """Step creation schema."""

    condition: Optional[Dict[str, Any]] = None
    on_condition_fail: Optional[Dict[str, Any]] = None


class FunnelStepUpdate(BaseModel):
    """Step update schema."""

    step_order: Optional[int] = Field(None, ge=0)
    name: Optional[str] = None
    delay_type: Optional[str] = None
    delay_value: Optional[int] = None
    actions: Optional[Dict[str, Any]] = None
    condition: Optional[Dict[str, Any]] = None


class FunnelStepResponse(BaseModel):
    """Step response schema."""

    id: str
    funnel_id: str
    step_order: int
    name: Optional[str]
    delay_type: str
    delay_value: Optional[int]
    delay_time: Optional[str]
    condition: Optional[Dict[str, Any]]
    actions: Dict[str, Any]
    on_condition_fail: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
