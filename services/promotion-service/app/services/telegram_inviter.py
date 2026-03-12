"""
Telegram inviter service using Telethon.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    UserPrivacyRestrictedError,
    UserChannelsTooMuchError,
    UserIsBlockedError,
    ChatWriteForbiddenError,
)
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser


class TelegramInviter:
    """Service for inviting users to Telegram chats."""

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
        session_name = f"inviter_{hash(self.session_string) % 10000}"
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

    async def invite_users(
        self,
        target_chat_id: str,
        users: List[Dict],
        max_invites: int = 50,
        delay_between_invites: float = 30.0,
    ) -> Dict:
        """
        Invite users to a Telegram chat.
        
        Args:
            target_chat_id: Chat ID or username to invite users to
            users: List of user dicts with telegram_id, username, first_name
            max_invites: Maximum number of invites to perform
            delay_between_invites: Delay between invites in seconds
            
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

        for i, user in enumerate(users[:max_invites]):
            try:
                # Get user entity
                user_entity = await self._get_user_entity(user)
                
                if not user_entity:
                    failed_count += 1
                    errors.append({
                        "user_id": user.get("telegram_id"),
                        "error": "User not found",
                    })
                    continue

                # Invite user
                await self.client(InviteToChannelRequest(
                    channel=target_entity,
                    users=[user_entity],
                ))

                success_count += 1

                # Delay between invites (anti-flood)
                if i < len(users) - 1:
                    await asyncio.sleep(delay_between_invites)

            except FloodWaitError as e:
                # Rate limited - wait and retry
                wait_time = e.seconds
                errors.append({
                    "user_id": user.get("telegram_id"),
                    "error": f"Flood wait: {wait_time}s",
                })
                failed_count += 1
                
                # Wait for flood timeout
                await asyncio.sleep(wait_time + 5)

            except UserPrivacyRestrictedError:
                # User has privacy settings that prevent invites
                errors.append({
                    "user_id": user.get("telegram_id"),
                    "error": "Privacy restricted",
                })
                failed_count += 1

            except UserChannelsTooMuchError:
                # User is in too many channels
                errors.append({
                    "user_id": user.get("telegram_id"),
                    "error": "User in too many channels",
                })
                failed_count += 1

            except UserIsBlockedError:
                # User blocked the bot
                errors.append({
                    "user_id": user.get("telegram_id"),
                    "error": "User blocked",
                })
                failed_count += 1

            except ChatWriteForbiddenError:
                # Can't write to chat
                errors.append({
                    "user_id": user.get("telegram_id"),
                    "error": "Chat write forbidden",
                })
                failed_count += 1
                # Stop inviting - chat is restricted
                break

            except Exception as e:
                errors.append({
                    "user_id": user.get("telegram_id"),
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

    async def _get_user_entity(self, user: Dict):
        """Get Telethon user entity from user dict."""
        try:
            # Try by username first
            if user.get("username"):
                return await self.client.get_entity(f"@{user['username']}")
            
            # Try by phone
            if user.get("phone"):
                return await self.client.get_entity(user["phone"])
            
            # Try by ID (requires knowing the user somehow)
            # This is a limitation - Telethon needs username or phone
            return None
            
        except Exception:
            return None

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
