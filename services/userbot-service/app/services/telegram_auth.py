"""
Telegram authorization service using Telethon.
"""

import hashlib
from typing import Optional

from telethon import TelegramClient
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneNumBannedError,
)
from telethon.tl.functions.auth import SendCodeRequest


class TelegramAuthService:
    """Service for Telegram userbot authorization."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone: str,
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client: Optional[TelegramClient] = None
        self.phone_code_hash: Optional[str] = None

    def _get_session_name(self) -> str:
        """Generate unique session name from phone."""
        return f"userbot_{hashlib.md5(self.phone.encode()).hexdigest()}"

    async def connect(self) -> None:
        """Connect to Telegram."""
        session_name = self._get_session_name()
        self.client = TelegramClient(
            session_name,
            self.api_id,
            self.api_hash,
        )
        await self.client.connect()

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def send_code(self) -> dict:
        """
        Send verification code to phone number.
        
        Returns:
            dict: {
                "success": bool,
                "phone_code_hash": str,
                "type": int,  # Code type (1=SMS, 5=call, etc.)
                "next_type": int | None,
                "timeout": int,
                "error": str | None
            }
        """
        try:
            if not self.client:
                await self.connect()

            result = await self.client(SendCodeRequest(self.phone, self.api_id, self.api_hash))
            
            self.phone_code_hash = result.phone_code_hash
            
            return {
                "success": True,
                "phone_code_hash": self.phone_code_hash,
                "type": result.type,
                "next_type": result.next_type,
                "timeout": result.timeout,
                "error": None,
            }

        except PhoneNumBannedError:
            return {
                "success": False,
                "phone_code_hash": None,
                "type": None,
                "next_type": None,
                "timeout": 0,
                "error": "Phone number is banned by Telegram",
            }
        except Exception as e:
            return {
                "success": False,
                "phone_code_hash": None,
                "type": None,
                "next_type": None,
                "timeout": 0,
                "error": str(e),
            }

    async def verify_code(self, code: str) -> dict:
        """
        Verify the code received from Telegram.
        
        Args:
            code: Verification code from Telegram (SMS or call)
            
        Returns:
            dict: {
                "success": bool,
                "session_string": str | None,
                "user_info": dict | None,
                "needs_2fa": bool,
                "error": str | None
            }
        """
        try:
            if not self.client:
                await self.connect()

            await self.client.sign_in(
                phone=self.phone,
                code=code,
                phone_code_hash=self.phone_code_hash,
            )

            # Get user info
            me = await self.client.get_me()
            
            # Get session string
            session_string = await self.client.session.save()

            return {
                "success": True,
                "session_string": session_string,
                "user_info": {
                    "id": me.id,
                    "first_name": me.first_name,
                    "last_name": me.last_name or "",
                    "username": me.username or "",
                    "phone": me.phone or "",
                },
                "needs_2fa": False,
                "error": None,
            }

        except SessionPasswordNeededError:
            return {
                "success": False,
                "session_string": None,
                "user_info": None,
                "needs_2fa": True,
                "error": "Two-factor authentication is enabled",
            }
        except PhoneCodeInvalidError:
            return {
                "success": False,
                "session_string": None,
                "user_info": None,
                "needs_2fa": False,
                "error": "Invalid verification code",
            }
        except Exception as e:
            return {
                "success": False,
                "session_string": None,
                "user_info": None,
                "needs_2fa": False,
                "error": str(e),
            }

    async def verify_2fa(self, password: str) -> dict:
        """
        Verify 2FA password.
        
        Args:
            password: 2FA password
            
        Returns:
            dict: {
                "success": bool,
                "session_string": str | None,
                "user_info": dict | None,
                "error": str | None
            }
        """
        try:
            if not self.client:
                await self.connect()

            await self.client.sign_in(password=password)

            # Get user info
            me = await self.client.get_me()
            
            # Get session string
            session_string = await self.client.session.save()

            return {
                "success": True,
                "session_string": session_string,
                "user_info": {
                    "id": me.id,
                    "first_name": me.first_name,
                    "last_name": me.last_name or "",
                    "username": me.username or "",
                    "phone": me.phone or "",
                },
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "session_string": None,
                "user_info": None,
                "error": str(e),
            }

    async def test_connection(self, session_string: str) -> dict:
        """
        Test if session string is valid.
        
        Args:
            session_string: Saved session string
            
        Returns:
            dict: {
                "success": bool,
                "user_info": dict | None,
                "error": str | None
            }
        """
        try:
            session_name = self._get_session_name()
            client = TelegramClient(session_name, self.api_id, self.api_hash)
            await client.connect()
            
            # Load session from string
            await client.session.restore(session_string)
            
            me = await client.get_me()
            
            await client.disconnect()

            return {
                "success": True,
                "user_info": {
                    "id": me.id,
                    "first_name": me.first_name,
                    "last_name": me.last_name or "",
                    "username": me.username or "",
                    "phone": me.phone or "",
                },
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "user_info": None,
                "error": str(e),
            }
