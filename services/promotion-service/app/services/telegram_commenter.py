"""
Telegram commenter service using Telethon.
"""

import asyncio
from typing import Dict, List, Optional

from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    ChatWriteForbiddenError,
    UserIsBlockedError,
)
from telethon.tl.functions.messages import SendMessageRequest


class TelegramCommenter:
    """Service for commenting on posts."""

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
        session_name = f"commenter_{hash(self.session_string) % 10000}"
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

    async def comment_posts(
        self,
        target_chat_id: str,
        comment_text: str,
        max_comments: int = 10,
        delay_between_comments: float = 60.0,
    ) -> Dict:
        """
        Comment on recent posts in a chat.
        
        Args:
            target_chat_id: Chat ID or username to comment in
            comment_text: Text to comment
            max_comments: Maximum number of comments to post
            delay_between_comments: Delay between comments in seconds
            
        Returns:
            dict: {
                "success": int,
                "failed": int,
                "errors": list
            }
        """
        if not self.client:
            await self.connect()

        # Get target entity
        try:
            target_entity = await self.client.get_entity(target_chat_id)
        except Exception as e:
            return {
                "success": 0,
                "failed": 0,
                "errors": [f"Failed to get target chat: {str(e)}"],
            }

        success_count = 0
        failed_count = 0
        errors = []

        # Get recent messages
        try:
            messages = await self.client.get_messages(
                target_entity,
                limit=max_comments,
            )
        except Exception as e:
            return {
                "success": 0,
                "failed": 0,
                "errors": [f"Failed to get messages: {str(e)}"],
            }

        for i, message in enumerate(messages):
            try:
                # Reply to message (comment)
                await self.client.send_message(
                    target_entity,
                    comment_text,
                    reply_to=message.id,
                )

                success_count += 1

                # Delay between comments (anti-flood)
                if i < len(messages) - 1:
                    await asyncio.sleep(delay_between_comments)

            except FloodWaitError as e:
                # Rate limited - wait and retry
                wait_time = e.seconds
                errors.append({
                    "message_id": message.id,
                    "error": f"Flood wait: {wait_time}s",
                })
                failed_count += 1
                
                # Wait for flood timeout
                await asyncio.sleep(wait_time + 5)

            except ChatWriteForbiddenError:
                # Can't write to chat
                errors.append({
                    "message_id": message.id,
                    "error": "Chat write forbidden",
                })
                failed_count += 1
                # Stop - chat is restricted
                break

            except UserIsBlockedError:
                # User blocked
                errors.append({
                    "message_id": message.id,
                    "error": "User blocked",
                })
                failed_count += 1

            except Exception as e:
                errors.append({
                    "message_id": message.id,
                    "error": str(e),
                })
                failed_count += 1

            # Small delay between attempts
            await asyncio.sleep(1)

        return {
            "success": success_count,
            "failed": failed_count,
            "errors": errors[:10],  # Limit errors in response
        }

    async def comment_on_multiple_chats(
        self,
        chats: List[str],
        comment_text: str,
        comments_per_chat: int = 5,
        delay_between_chats: float = 120.0,
    ) -> Dict:
        """
        Comment on multiple chats.
        
        Args:
            chats: List of chat IDs or usernames
            comment_text: Text to comment
            comments_per_chat: Number of comments per chat
            delay_between_chats: Delay between chats in seconds
            
        Returns:
            dict: {
                "success": int,
                "failed": int,
                "errors": list
            }
        """
        if not self.client:
            await self.connect()

        total_success = 0
        total_failed = 0
        all_errors = []

        for chat_id in chats:
            result = await self.comment_posts(
                target_chat_id=chat_id,
                comment_text=comment_text,
                max_comments=comments_per_chat,
                delay_between_comments=30.0,
            )

            total_success += result["success"]
            total_failed += result["failed"]
            all_errors.extend(result["errors"])

            # Delay between chats
            if chat_id != chats[-1]:
                await asyncio.sleep(delay_between_chats)

        return {
            "success": total_success,
            "failed": total_failed,
            "errors": all_errors[:20],  # Limit errors in response
        }

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
