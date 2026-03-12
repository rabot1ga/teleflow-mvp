"""
Telegram parser service using Telethon.
"""

import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator, Dict, List, Optional

from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsRecent, User


class TelegramParser:
    """Service for parsing users from Telegram chats."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: str,
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.client: Optional[TelegramClient] = None

    async def connect(self) -> None:
        """Connect to Telegram using session string."""
        session_name = f"parser_{hash(self.session_string) % 10000}"
        self.client = TelegramClient(session_name, self.api_id, self.api_hash)
        await self.client.connect()
        
        # Load session from string
        await self.client.session.restore(self.session_string)
        
        # Check if authorized
        if not await self.client.is_user_authorized():
            raise ValueError("Session is not authorized")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def get_chat_info(self, chat_id: str) -> Dict:
        """
        Get chat information.
        
        Args:
            chat_id: Chat ID or username (e.g., "@channel" or "-1001234567890")
            
        Returns:
            dict: Chat information
        """
        if not self.client:
            await self.connect()

        entity = await self.client.get_entity(chat_id)
        
        return {
            "id": entity.id,
            "title": getattr(entity, "title", getattr(entity, "username", "Unknown")),
            "username": getattr(entity, "username", None),
            "participants_count": getattr(entity, "participants_count", 0),
        }

    async def parse_users(
        self,
        chat_id: str,
        limit: int = 1000,
        offset: int = 0,
        filter_active_days: Optional[int] = None,
        filter_has_photo: Optional[bool] = None,
        filter_is_premium: Optional[bool] = None,
        filter_is_bot: bool = False,
    ) -> AsyncGenerator[Dict, None]:
        """
        Parse users from a Telegram chat.
        
        Args:
            chat_id: Chat ID or username
            limit: Maximum number of users to parse
            offset: Offset for pagination
            filter_active_days: Filter users active in last N days (None = no filter)
            filter_has_photo: Filter users with photo (None = no filter)
            filter_is_premium: Filter premium users (None = no filter)
            filter_is_bot: Include bots (default False)
            
        Yields:
            dict: User information
        """
        if not self.client:
            await self.connect()

        entity = await self.client.get_entity(chat_id)
        
        # Get participants
        offset_id = 0
        count = 0
        
        async for participant in self.client.iter_participants(
            entity,
            limit=limit,
            offset=offset,
        ):
            if count >= limit:
                break
            
            # Skip bots if requested
            if not filter_is_bot and participant.bot:
                continue
            
            # Apply filters
            user_info = self._extract_user_info(participant)
            
            if not self._matches_filters(
                user_info,
                filter_active_days,
                filter_has_photo,
                filter_is_premium,
            ):
                continue
            
            yield user_info
            count += 1
            
            # Yield control to event loop
            await asyncio.sleep(0)

    def _extract_user_info(self, user: User) -> Dict:
        """Extract user information from Telethon User object."""
        return {
            "telegram_id": user.id,
            "username": user.username,
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "phone": user.phone,
            "is_bot": user.bot,
            "is_premium": getattr(user, "premium", False),
            "has_photo": bool(getattr(user, "photo", None)),
            "last_seen_days": self._calculate_last_seen_days(user),
        }

    def _calculate_last_seen_days(self, user: User) -> Optional[int]:
        """Calculate days since user was last seen."""
        status = getattr(user, "status", None)
        if not status:
            return None
        
        from telethon.tl.types import (
            UserStatusOnline,
            UserStatusOffline,
            UserStatusRecently,
            UserStatusLastMonth,
            UserStatusLastWeek,
        )
        
        if isinstance(status, UserStatusOnline):
            return 0
        elif isinstance(status, UserStatusOffline):
            if status.was_online:
                delta = datetime.now() - status.was_online
                return delta.days
        elif isinstance(status, UserStatusRecently):
            return 1
        elif isinstance(status, UserStatusLastWeek):
            return 7
        elif isinstance(status, UserStatusLastMonth):
            return 30
        
        return None

    def _matches_filters(
        self,
        user_info: Dict,
        filter_active_days: Optional[int],
        filter_has_photo: Optional[bool],
        filter_is_premium: Optional[bool],
    ) -> bool:
        """Check if user matches all filters."""
        # Active days filter
        if filter_active_days is not None:
            last_seen = user_info.get("last_seen_days")
            if last_seen is None or last_seen > filter_active_days:
                return False
        
        # Has photo filter
        if filter_has_photo is not None:
            if user_info.get("has_photo") != filter_has_photo:
                return False
        
        # Premium filter
        if filter_is_premium is not None:
            if user_info.get("is_premium") != filter_is_premium:
                return False
        
        return True

    async def test_connection(self) -> Dict:
        """Test if connection is working."""
        if not self.client:
            await self.connect()
        
        me = await self.client.get_me()
        
        return {
            "success": True,
            "user_id": me.id,
            "username": me.username,
            "first_name": me.first_name,
        }
