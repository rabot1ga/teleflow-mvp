"""
FunnelUser schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class FunnelUserCreate(BaseModel):
    """Funnel user creation schema."""

    telegram_user_id: int
    source: Optional[str] = None


class FunnelUserResponse(BaseModel):
    """Funnel user response schema."""

    id: str
    funnel_id: str
    telegram_user_id: int
    current_step_id: Optional[str]
    status: str
    user_data: dict
    tags: List[str]
    source: Optional[str]
    entered_at: datetime
    last_action_at: Optional[datetime]
    completed_at: Optional[datetime]
    next_step_at: Optional[datetime]

    class Config:
        from_attributes = True
