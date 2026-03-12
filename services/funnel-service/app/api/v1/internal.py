"""
Internal API endpoints for funnel triggers.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.dependencies import get_async_session
from app.models.funnel import Funnel
from app.models.funnel_user import FunnelUser
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/funnels", tags=["Internal Funnels"])


class TriggerFunnelRequest(BaseModel):
    telegram_user_id: int
    trigger_type: str
    trigger_value: str


@router.post(
    "/trigger",
    response_model=StandardResponse[dict],
    summary="Trigger funnel (internal)",
)
async def trigger_funnel(
    data: TriggerFunnelRequest,
    db=Depends(get_async_session),
) -> StandardResponse[dict]:
    """Trigger funnel for a user based on trigger type/value."""
    # Find matching funnel
    result = await db.execute(
        select(Funnel)
        .where(Funnel.trigger_type == data.trigger_type)
        .where(Funnel.is_active == True)
        .limit(1)
    )
    funnel = result.scalar_one_or_none()

    if not funnel:
        # No matching funnel - return without error
        return StandardResponse(
            data={"triggered": False, "reason": "no_matching_funnel"},
            meta=ResponseMeta(request_id=""),
        )

    # Check if user already in this funnel
    existing = await db.execute(
        select(FunnelUser)
        .where(FunnelUser.funnel_id == funnel.id)
        .where(FunnelUser.telegram_user_id == data.telegram_user_id)
    )
    if existing.scalar_one_or_none():
        # User already in funnel
        return StandardResponse(
            data={"triggered": False, "reason": "already_in_funnel"},
            meta=ResponseMeta(request_id=""),
        )

    # Create funnel user
    funnel_user = FunnelUser(
        funnel_id=funnel.id,
        telegram_user_id=data.telegram_user_id,
        status="active",
        entered_at=datetime.utcnow(),
        source=data.trigger_value,
    )

    db.add(funnel_user)
    await db.flush()

    # Trigger first step
    from app.tasks import process_funnel_step
    process_funnel_step.delay(funnel_user.id, "")

    return StandardResponse(
        data={
            "triggered": True,
            "funnel_id": funnel.id,
            "funnel_name": funnel.name,
            "user_id": funnel_user.id,
        },
        meta=ResponseMeta(request_id=""),
    )
