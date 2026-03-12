"""
Event consumers for Redis Pub/Sub.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List

import redis.asyncio as redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import AnalyticsEvent, AnalyticsDaily


class EventConsumer:
    """Consumer for analytics events from Redis Pub/Sub."""

    # Event types we're interested in
    EVENTS = [
        "article.created",
        "article.approved",
        "article.rejected",
        "article.published",
        "funnel.user_entered",
        "funnel.step_completed",
        "funnel.completed",
        "user.subscribed",
        "broadcast.sent",
        "broadcast.delivered",
        "promotion.task_completed",
        "userbot.action_completed",
    ]

    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis_url = redis_url
        self.redis: redis.Redis | None = None
        self.pubsub: redis.client.PubSub | None = None

    async def connect(self) -> None:
        """Connect to Redis and subscribe to events."""
        self.redis = redis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()
        
        # Subscribe to all event channels
        await self.pubsub.psubscribe(*[f"events:{event}" for event in self.EVENTS])

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.pubsub:
            await self.pubsub.punsubscribe()
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()

    async def consume_events(self, session_factory) -> None:
        """Consume events from Redis and save to database."""
        while True:
            try:
                message = await self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0,
                )
                
                if message and message["type"] == "pmessage":
                    channel = message["channel"]
                    data = json.loads(message["data"])
                    
                    # Parse event type from channel
                    event_type = channel.replace("events:", "")
                    
                    # Save event
                    await self._save_event(session_factory, event_type, data)
                    
                    # Update daily stats
                    await self._update_daily_stats(session_factory, event_type, data)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log error but continue consuming
                print(f"Error consuming event: {e}")
                await asyncio.sleep(1)

    async def _save_event(
        self,
        session_factory,
        event_type: str,
        data: Dict,
    ) -> None:
        """Save raw event to database."""
        async with session_factory() as session:
            event = AnalyticsEvent(
                project_id=data.get("project_id"),
                event_type=event_type,
                entity_type=data.get("entity_type"),
                entity_id=data.get("entity_id"),
                payload=data,
                user_id=data.get("user_id"),
                event_timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat())),
            )
            session.add(event)
            await session.commit()

    async def _update_daily_stats(
        self,
        session_factory,
        event_type: str,
        data: Dict,
    ) -> None:
        """Update daily aggregated stats."""
        async with session_factory() as session:
            project_id = data.get("project_id")
            if not project_id:
                return
            
            # Get today's date
            today = datetime.utcnow().date()
            
            # Get or create daily record
            result = await session.execute(
                select(AnalyticsDaily).where(
                    AnalyticsDaily.project_id == project_id,
                    AnalyticsDaily.date == today,
                )
            )
            daily = result.scalar_one_or_none()
            
            if not daily:
                daily = AnalyticsDaily(
                    project_id=project_id,
                    date=today,
                )
                session.add(daily)
                await session.flush()
            
            # Update counters based on event type
            self._update_counters(daily, event_type, data)
            
            await session.commit()

    def _update_counters(
        self,
        daily: AnalyticsDaily,
        event_type: str,
        data: Dict,
    ) -> None:
        """Update daily counters based on event type."""
        if event_type == "article.created":
            daily.articles_created += 1
        elif event_type == "article.approved":
            daily.articles_approved += 1
        elif event_type == "article.rejected":
            daily.articles_rejected += 1
        elif event_type == "article.published":
            daily.articles_published += 1
        elif event_type == "funnel.user_entered":
            daily.funnel_entries += 1
        elif event_type == "funnel.completed":
            daily.funnel_completions += 1
        elif event_type in ("broadcast.sent", "broadcast.delivered"):
            daily.broadcasts_sent += 1
            daily.messages_delivered += data.get("count", 1)
        elif event_type == "promotion.task_completed":
            daily.users_parsed += data.get("parsed", 0)
            daily.users_invited += data.get("invited", 0)
        elif event_type == "userbot.action_completed":
            daily.userbot_actions += 1
        elif event_type.startswith("ai."):
            daily.ai_requests += 1
            daily.ai_tokens_used += data.get("tokens", 0)
