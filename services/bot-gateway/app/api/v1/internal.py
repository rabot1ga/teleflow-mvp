"""
Bot Gateway internal API for other services.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.bot import get_bot
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/internal/bot", tags=["Internal Bot API"])


class SendMessageRequest(BaseModel):
    chat_id: int
    text: str
    parse_mode: str = "HTML"
    disable_preview: bool = False


class SendPhotoRequest(BaseModel):
    chat_id: int
    photo: str  # URL or file_id
    caption: str = ""
    parse_mode: str = "HTML"


@router.post(
    "/send-message",
    response_model=StandardResponse[dict],
    summary="Send message (internal)",
)
async def send_message(data: SendMessageRequest) -> StandardResponse[dict]:
    """Send text message via Telegram Bot API."""
    bot = get_bot()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot not configured",
        )
    
    try:
        result = await bot.send_message(
            chat_id=data.chat_id,
            text=data.text,
            parse_mode=data.parse_mode,
            disable_web_page_preview=data.disable_preview,
        )
        
        return StandardResponse(
            data={
                "message_id": result.message_id,
                "chat_id": result.chat.id,
            },
            meta=ResponseMeta(request_id=""),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/send-photo",
    response_model=StandardResponse[dict],
    summary="Send photo (internal)",
)
async def send_photo(data: SendPhotoRequest) -> StandardResponse[dict]:
    """Send photo via Telegram Bot API."""
    bot = get_bot()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot not configured",
        )
    
    try:
        result = await bot.send_photo(
            chat_id=data.chat_id,
            photo=data.photo,
            caption=data.caption,
            parse_mode=data.parse_mode,
        )
        
        return StandardResponse(
            data={
                "message_id": result.message_id,
                "chat_id": result.chat.id,
            },
            meta=ResponseMeta(request_id=""),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/check-subscription",
    response_model=StandardResponse[bool],
    summary="Check user subscription (internal)",
)
async def check_subscription(
    user_id: int,
    channel_id: int,
) -> StandardResponse[bool]:
    """Check if user is subscribed to channel."""
    bot = get_bot()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot not configured",
        )
    
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        is_subscribed = member.status in ["member", "administrator", "creator"]
        
        return StandardResponse(
            data=is_subscribed,
            meta=ResponseMeta(request_id=""),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
