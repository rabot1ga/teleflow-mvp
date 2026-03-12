"""
Celery tasks for Funnel Service.
"""

import asyncio
from datetime import datetime, timedelta

import httpx
import structlog
from sqlalchemy import select

from app.celery_app import celery_app
from app.database import async_session_factory
from app.models.broadcast import Broadcast
from app.models.funnel import Funnel
from app.models.funnel_step import FunnelStep
from app.models.funnel_user import FunnelUser

logger = structlog.get_logger()


@celery_app.task
def process_funnel_step(user_id: str, step_id: str) -> dict:
    """
    Process next step in funnel for a user.
    """
    async def _process():
        async with async_session_factory() as db:
            # Get funnel user
            result = await db.execute(
                select(FunnelUser).where(FunnelUser.id == user_id)
            )
            funnel_user = result.scalar_one_or_none()

            if not funnel_user:
                logger.error("funnel_user_not_found", user_id=user_id)
                return {"status": "error", "error": "User not found"}

            # Get current step
            if not funnel_user.current_step_id:
                # Get first step
                result = await db.execute(
                    select(FunnelStep)
                    .where(FunnelStep.funnel_id == funnel_user.funnel_id)
                    .order_by(FunnelStep.step_order)
                    .limit(1)
                )
                step = result.scalar_one_or_none()
                if not step:
                    return {"status": "completed", "reason": "no_steps"}
            else:
                result = await db.execute(
                    select(FunnelStep).where(FunnelStep.id == funnel_user.current_step_id)
                )
                step = result.scalar_one_or_none()
                if not step:
                    return {"status": "completed", "reason": "step_not_found"}

            # Execute actions
            await execute_step_actions(funnel_user, step)

            # Schedule next step
            next_step = await get_next_step(db, funnel_user.funnel_id, step.step_order)
            if next_step:
                funnel_user.current_step_id = next_step.id
                funnel_user.next_step_at = calculate_next_step_time(next_step)
                logger.info(
                    "funnel_step_scheduled",
                    user_id=user_id,
                    next_step_id=next_step.id,
                    next_step_at=funnel_user.next_step_at,
                )
            else:
                funnel_user.status = "completed"
                funnel_user.completed_at = datetime.utcnow()
                logger.info("funnel_completed", user_id=user_id)

            funnel_user.last_action_at = datetime.utcnow()
            await db.flush()

            return {"status": "processed", "step_id": step.id}

    return asyncio.run(_process())


@celery_app.task
def check_pending_steps() -> dict:
    """
    Check and process pending funnel steps.
    """
    async def _check():
        async with async_session_factory() as db:
            now = datetime.utcnow()

            # Get users with pending steps
            result = await db.execute(
                select(FunnelUser)
                .where(FunnelUser.status == "active")
                .where(FunnelUser.next_step_at <= now)
                .limit(100)
            )
            users = result.scalars().all()

            logger.info("pending_steps_check", count=len(users))

            # Process each user
            for user in users:
                if user.current_step_id:
                    process_funnel_step.delay(user.id, user.current_step_id)
                else:
                    process_funnel_step.delay(user.id, "")

            return {
                "status": "checked",
                "users_processed": len(users),
            }

    return asyncio.run(_check())


@celery_app.task(bind=True, max_retries=3)
def execute_broadcast(self, broadcast_id: str) -> dict:
    """
    Execute broadcast to funnel users.
    
    Steps:
    1. Get broadcast
    2. Get recipients based on filter
    3. Send messages in batches
    4. Update stats
    """
    async def _execute():
        async with async_session_factory() as db:
            # Get broadcast
            result = await db.execute(
                select(Broadcast).where(Broadcast.id == broadcast_id)
            )
            broadcast = result.scalar_one_or_none()

            if not broadcast:
                logger.error("broadcast_not_found", broadcast_id=broadcast_id)
                return {"status": "error", "error": "Broadcast not found"}

            # Update status
            broadcast.status = "running"
            await db.flush()

            try:
                # Get recipients
                recipients = await get_broadcast_recipients(db, broadcast)
                total = len(recipients)
                
                logger.info(
                    "broadcast_started",
                    broadcast_id=broadcast_id,
                    total_recipients=total,
                )

                # Send messages in batches
                batch_size = 10
                sent = 0
                delivered = 0
                failed = 0

                for i in range(0, total, batch_size):
                    batch = recipients[i:i + batch_size]
                    
                    for recipient in batch:
                        success = await send_broadcast_message(
                            recipient["telegram_user_id"],
                            broadcast.message_text,
                            broadcast.message_type,
                            broadcast.message_media_url,
                        )
                        
                        if success:
                            delivered += 1
                        else:
                            failed += 1
                        sent += 1

                    # Update progress
                    broadcast.sent = sent
                    broadcast.delivered = delivered
                    broadcast.failed = failed
                    await db.flush()
                    
                    # Rate limiting delay
                    await asyncio.sleep(1.0 / broadcast.send_rate)

                # Complete
                broadcast.status = "completed"
                broadcast.completed_at = datetime.utcnow()
                broadcast.total_recipients = total
                await db.flush()

                logger.info(
                    "broadcast_completed",
                    broadcast_id=broadcast_id,
                    sent=sent,
                    delivered=delivered,
                    failed=failed,
                )

                return {
                    "status": "completed",
                    "sent": sent,
                    "delivered": delivered,
                    "failed": failed,
                }

            except Exception as e:
                broadcast.status = "failed"
                broadcast.error = str(e)
                await db.flush()
                
                logger.error("broadcast_failed", broadcast_id=broadcast_id, error=str(e))
                
                # Retry
                raise self.retry(exc=e, countdown=60)

    return asyncio.run(_execute())


async def get_broadcast_recipients(db, broadcast: Broadcast) -> list:
    """Get recipients based on broadcast filter."""
    filter_config = broadcast.recipient_filter
    filter_type = filter_config.get("type", "all")

    if filter_type == "all":
        # Get all funnel users
        result = await db.execute(
            select(FunnelUser.telegram_user_id)
            .distinct()
        )
        return [{"telegram_user_id": row[0]} for row in result.all()]
    
    elif filter_type == "funnel":
        # Get users from specific funnel
        funnel_id = filter_config.get("funnel_id")
        status = filter_config.get("status")
        
        query = select(FunnelUser.telegram_user_id).where(
            FunnelUser.funnel_id == funnel_id
        )
        if status:
            query = query.where(FunnelUser.status == status)
        
        result = await db.execute(query)
        return [{"telegram_user_id": row[0]} for row in result.all()]
    
    elif filter_type == "tags":
        # Get users with specific tags
        tags = filter_config.get("tags", [])
        operator = filter_config.get("operator", "any")
        
        if operator == "all":
            # Users with ALL tags
            result = await db.execute(
                select(FunnelUser.telegram_user_id)
                .where(FunnelUser.tags.contains(tags))
            )
        else:
            # Users with ANY tag
            result = await db.execute(
                select(FunnelUser.telegram_user_id)
                .where(
                    FunnelUser.tags.overlap(tags)  # PostgreSQL array overlap
                )
            )
        
        return [{"telegram_user_id": row[0]} for row in result.all()]
    
    elif filter_type == "list":
        # Specific user IDs
        user_ids = filter_config.get("user_ids", [])
        return [{"telegram_user_id": uid} for uid in user_ids]
    
    return []


async def send_broadcast_message(
    telegram_user_id: int,
    message_text: str,
    message_type: str = "text",
    message_media_url: str = None,
) -> bool:
    """Send message to Telegram user via Bot Gateway."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if message_type == "photo" and message_media_url:
                await client.post(
                    "http://bot-gateway:8006/internal/bot/send-photo",
                    json={
                        "chat_id": telegram_user_id,
                        "photo": message_media_url,
                        "caption": message_text,
                        "parse_mode": "HTML",
                    }
                )
            else:
                await client.post(
                    "http://bot-gateway:8006/internal/bot/send-message",
                    json={
                        "chat_id": telegram_user_id,
                        "text": message_text,
                        "parse_mode": "HTML",
                    }
                )
            return True
    except Exception as e:
        logger.error(
            "failed_to_send_broadcast",
            user_id=telegram_user_id,
            error=str(e),
        )
        return False


async def execute_step_actions(funnel_user: FunnelUser, step: FunnelStep):
    """Execute actions for a funnel step."""
    actions = step.actions or {}
    action_type = actions.get("type")

    if action_type == "send_message":
        await send_message_to_user(
            funnel_user.telegram_user_id,
            actions.get("text", ""),
        )
    elif action_type == "send_lead_magnet":
        await send_lead_magnet(
            funnel_user.telegram_user_id,
            actions.get("magnet_id"),
        )


async def send_message_to_user(telegram_user_id: int, text: str):
    """Send message to Telegram user via Bot Gateway."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(
                "http://bot-gateway:8006/internal/bot/send-message",
                json={
                    "chat_id": telegram_user_id,
                    "text": text,
                    "parse_mode": "HTML",
                }
            )
            logger.info("message_sent", user_id=telegram_user_id)
    except Exception as e:
        logger.error("failed_to_send_message", user_id=telegram_user_id, error=str(e))


async def send_lead_magnet(telegram_user_id: int, magnet_id: str):
    """Send lead magnet to user."""
    # TODO: Get magnet from DB and send
    logger.info("lead_magnet_sent", user_id=telegram_user_id, magnet_id=magnet_id)


async def get_next_step(db, funnel_id: str, current_order: int):
    """Get next step in funnel."""
    result = await db.execute(
        select(FunnelStep)
        .where(FunnelStep.funnel_id == funnel_id)
        .where(FunnelStep.step_order > current_order)
        .order_by(FunnelStep.step_order)
        .limit(1)
    )
    return result.scalar_one_or_none()


def calculate_next_step_time(step: FunnelStep) -> datetime:
    """Calculate when next step should be executed."""
    now = datetime.utcnow()
    delay_type = step.delay_type or "immediate"
    delay_value = step.delay_value or 0

    if delay_type == "immediate":
        return now
    elif delay_type == "seconds":
        return now + timedelta(seconds=delay_value)
    elif delay_type == "minutes":
        return now + timedelta(minutes=delay_value)
    elif delay_type == "hours":
        return now + timedelta(hours=delay_value)
    elif delay_type == "days":
        return now + timedelta(days=delay_value)
    else:
        return now
