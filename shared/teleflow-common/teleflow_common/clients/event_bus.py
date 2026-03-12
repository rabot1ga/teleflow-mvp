"""
Event Bus for Redis Pub/Sub.
"""

import json
from typing import Any, Callable, Optional

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger()


class EventBus:
    """
    Redis Pub/Sub wrapper for async event communication.

    Usage:
        # Publish
        await event_bus.publish("article.created", {"article_id": "uuid"})

        # Subscribe
        @event_bus.subscribe("article.created")
        async def handle_article_created(event: dict):
            ...
    """

    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis_url = redis_url
        self._redis: Optional[Redis] = None
        self._subscribers: dict[str, list[Callable]] = {}
        self._pubsub = None
        self._running = False

    async def connect(self) -> None:
        """Connect to Redis."""
        self._redis = Redis.from_url(self.redis_url, decode_responses=True)
        logger.info("event_bus_connected", url=self.redis_url)

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        self._running = False
        if self._pubsub:
            await self._pubsub.close()
        if self._redis:
            await self._redis.close()
        logger.info("event_bus_disconnected")

    async def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        """
        Publish an event.

        Args:
            event_type: Event type (e.g., "article.created")
            payload: Event payload data
        """
        if not self._redis:
            await self.connect()

        message = json.dumps({"type": event_type, "payload": payload})
        await self._redis.publish(f"teleflow:{event_type}", message)

        logger.debug(
            "event_published",
            event_type=event_type,
            payload_keys=list(payload.keys()),
        )

    def subscribe(self, event_type: str) -> Callable:
        """
        Decorator to subscribe a function to an event.

        Usage:
            @event_bus.subscribe("article.created")
            async def handle_article_created(event: dict):
                ...
        """

        def decorator(func: Callable) -> Callable:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(func)
            logger.info("event_subscribed", event_type=event_type, handler=func.__name__)
            return func

        return decorator

    async def start_listening(self) -> None:
        """Start listening for events (run in background task)."""
        if not self._redis:
            await self.connect()

        self._running = True
        self._pubsub = self._redis.pubsub()

        # Subscribe to all registered channels
        channels = [f"teleflow:{event_type}" for event_type in self._subscribers.keys()]
        if channels:
            await self._pubsub.subscribe(*channels)
            logger.info("event_bus_listening", channels=channels)

        # Listen for messages
        while self._running:
            try:
                message = await self._pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0,
                )
                if message and message["type"] == "message":
                    await self._handle_message(message)
            except Exception as e:
                logger.error("event_bus_listen_error", error=str(e))

    async def _handle_message(self, message: dict[str, Any]) -> None:
        """Handle incoming message."""
        channel = message["channel"]
        data = json.loads(message["data"])

        event_type = data.get("type")
        payload = data.get("payload")

        if not event_type:
            logger.warning("event_missing_type", channel=channel)
            return

        # Get subscribers
        handlers = self._subscribers.get(event_type, [])

        if not handlers:
            logger.debug("event_no_handlers", event_type=event_type)
            return

        # Call handlers
        for handler in handlers:
            try:
                await handler(payload)
            except Exception as e:
                logger.error(
                    "event_handler_error",
                    event_type=event_type,
                    handler=handler.__name__,
                    error=str(e),
                )

    def get_subscribers(self, event_type: str) -> list[Callable]:
        """Get all handlers for an event type."""
        return self._subscribers.get(event_type, [])


# Global event bus instance (to be initialized per service)
_event_bus: Optional[EventBus] = None


def get_event_bus(redis_url: str = "redis://redis:6379/0") -> EventBus:
    """Get or create global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus(redis_url)
    return _event_bus
