"""
Telegram masslook service using Telethon.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telethon import TelegramClient
from telethon.tl.types import PeerChannel, PeerUser


class TelegramMasslooker:
    """Service for mass viewing stories (masslook)."""

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
        session_name = f"masslook_{hash(self.session_string) % 10000}"
        self.client = TelegramClient(session_name, self.api_id, self.api_hash)
        await self.client.connect()
        await self.client.session.restore(self.session_string)
        
        if not await self.client.is_user_authorized():
            raise ValueError("Session is not authorized")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def view_stories(
        self,
        target_usernames: List[str],
        stories_to_look: int = 5,
        delay_between_views: float = 5.0,
    ) -> Dict:
        """
        View stories from target users (masslook).
        
        Args:
            target_usernames: List of usernames to view stories from
            stories_to_look: Number of stories to view per user
            delay_between_views: Delay between story views in seconds
            
        Returns:
            dict: {
                "success": int,
                "failed": int,
                "errors": list
            }
        """
        if not self.client:
            await self.connect()

        success_count = 0
        failed_count = 0
        errors = []

        for username in target_usernames:
            try:
                # Get user entity
                entity = await self.client.get_entity(f"@{username}")
                
                # Get user stories
                # Note: Telethon story API is limited, this is a placeholder
                # In real implementation, you would use stories API
                stories = await self._get_user_stories(entity)
                
                if not stories:
                    failed_count += 1
                    errors.append({
                        "username": username,
                        "error": "No stories available",
                    })
                    continue

                # View stories
                viewed = 0
                for story in stories[:stories_to_look]:
                    try:
                        await self._view_story(entity, story)
                        viewed += 1
                        success_count += 1
                        
                        # Delay between views
                        if viewed < len(stories[:stories_to_look]):
                            await asyncio.sleep(delay_between_views)
                            
                    except Exception as e:
                        failed_count += 1
                        errors.append({
                            "username": username,
                            "error": f"Story view failed: {str(e)}",
                        })

                if viewed == 0:
                    failed_count += 1
                    errors.append({
                        "username": username,
                        "error": "Failed to view any stories",
                    })

            except Exception as e:
                failed_count += 1
                errors.append({
                    "username": username,
                    "error": str(e),
                })

            # Small delay between users
            await asyncio.sleep(2)

        return {
            "success": success_count,
            "failed": failed_count,
            "errors": errors[:10],  # Limit errors in response
        }

    async def _get_user_stories(self, entity) -> List:
        """
        Get stories from user.
        
        Note: Telethon's story API is limited. This is a placeholder
        for the actual implementation which would use the stories API.
        """
        # TODO: Implement actual story fetching when Telethon supports it
        # For now, return empty list
        return []

    async def _view_story(self, entity, story) -> None:
        """
        View a single story.
        
        Note: This is a placeholder for the actual implementation.
        """
        # TODO: Implement actual story view when Telethon supports it
        pass

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
