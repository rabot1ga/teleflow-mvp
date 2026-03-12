"""
Promotion task executor.
"""

import os
from datetime import datetime
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.promotion import PromotionTask, PromotionTaskStatus, ParsedUser
from app.services.telegram_parser import TelegramParser
from app.services.telegram_inviter import TelegramInviter
from app.services.telegram_masslooker import TelegramMasslooker
from app.services.telegram_commenter import TelegramCommenter


class PromotionExecutor:
    """Executor for promotion tasks."""

    def __init__(self, task: PromotionTask, session: AsyncSession):
        self.task = task
        self.session = session
        self.api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")

    async def execute_parse(self) -> Dict:
        """
        Execute parsing task.
        
        Returns:
            dict: {
                "processed": int,
                "success": int,
                "failed": int
            }
        """
        if not self.task.source_chat_id:
            raise ValueError("source_chat_id is required for parse task")
        
        # Get userbot accounts for parsing
        userbot_accounts = await self._get_userbot_accounts()
        
        if not userbot_accounts:
            raise ValueError("No userbot accounts available for parsing")
        
        # Use first available account
        account = userbot_accounts[0]
        
        # Get session string
        from cryptography.fernet import Fernet
        encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")
        fernet = Fernet(encryption_key.encode())
        session_string = fernet.decrypt(account.session_string.encode()).decode()
        
        # Create parser
        parser = TelegramParser(
            api_id=self.api_id,
            api_hash=self.api_hash,
            session_string=session_string,
        )
        
        try:
            await parser.connect()
            
            # Get parse config
            config = self.task.config or {}
            limit = config.get("limit", 1000)
            filter_active_days = config.get("filter_active_days")
            filter_has_photo = config.get("filter_has_photo")
            filter_is_premium = config.get("filter_is_premium")
            
            # Parse users
            success_count = 0
            failed_count = 0
            
            async for user_data in parser.parse_users(
                chat_id=self.task.source_chat_id,
                limit=limit,
                filter_active_days=filter_active_days,
                filter_has_photo=filter_has_photo,
                filter_is_premium=filter_is_premium,
                filter_is_bot=False,
            ):
                try:
                    # Save to database
                    parsed_user = ParsedUser(
                        task_id=self.task.id,
                        project_id=self.task.project_id,
                        telegram_id=user_data["telegram_id"],
                        username=user_data["username"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        phone=user_data["phone"],
                        is_bot=user_data["is_bot"],
                        is_premium=user_data["is_premium"],
                        has_photo=user_data["has_photo"],
                        last_seen_days=user_data["last_seen_days"],
                    )
                    self.session.add(parsed_user)
                    success_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    # Log error but continue
                
                # Commit every 100 users
                if success_count % 100 == 0:
                    await self.session.commit()
            
            # Final commit
            await self.session.commit()
            
            # Update task stats
            self.task.total_count = success_count + failed_count
            self.task.processed_count = success_count + failed_count
            self.task.success_count = success_count
            self.task.failed_count = failed_count
            
            return {
                "processed": success_count + failed_count,
                "success": success_count,
                "failed": failed_count,
            }
            
        finally:
            await parser.disconnect()

    async def execute_invite(self) -> Dict:
        """
        Execute invite task.
        
        Returns:
            dict: {
                "processed": int,
                "success": int,
                "failed": int
            }
        """
        if not self.task.target_chat_id:
            raise ValueError("target_chat_id is required for invite task")
        
        # Get userbot accounts for inviting
        userbot_accounts = await self._get_userbot_accounts()
        
        if not userbot_accounts:
            raise ValueError("No userbot accounts available for inviting")
        
        # Get users to invite (not invited yet)
        result = await self.session.execute(
            select(ParsedUser)
            .where(ParsedUser.task_id == self.task.id)
            .where(ParsedUser.is_invited == False)
            .limit(100)  # Batch size
        )
        users_to_invite = result.scalars().all()
        
        if not users_to_invite:
            return {
                "processed": 0,
                "success": 0,
                "failed": 0,
                "message": "No users to invite",
            }
        
        # Use first available account for inviting
        account = userbot_accounts[0]
        
        # Get session string
        from cryptography.fernet import Fernet
        encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")
        fernet = Fernet(encryption_key.encode())
        session_string = fernet.decrypt(account.session_string.encode()).decode()
        
        # Create inviter
        inviter = TelegramInviter(
            api_id=self.api_id,
            api_hash=self.api_hash,
            session_string=session_string,
        )
        
        try:
            await inviter.connect()
            
            # Get invite config
            config = self.task.config or {}
            max_invites = config.get("max_invites_per_account", 50)
            delay = config.get("delay_between_invites_sec", 30)
            
            # Convert users to dict format
            users_data = [
                {
                    "telegram_id": user.telegram_id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "phone": user.phone,
                }
                for user in users_to_invite
            ]
            
            # Invite users
            invite_result = await inviter.invite_users(
                target_chat_id=self.task.target_chat_id,
                users=users_data,
                max_invites=max_invites,
                delay_between_invites=delay,
            )
            
            # Update user records
            success_ids = set()
            for error in invite_result.get("errors", []):
                user_id = error.get("user_id")
                if user_id:
                    # Find and mark user
                    for user in users_to_invite:
                        if user.telegram_id == user_id:
                            user.is_invited = False
                            user.invite_error = error.get("error", "Unknown error")
                            break
            
            # Mark successfully invited users
            for user in users_to_invite:
                if user.telegram_id not in [e.get("user_id") for e in invite_result.get("errors", [])]:
                    user.is_invited = True
                    user.invited_at = datetime.utcnow()
                    user.invite_error = None
                    success_ids.add(user.telegram_id)
            
            await self.session.commit()
            
            return {
                "processed": len(users_to_invite),
                "success": invite_result["success"],
                "failed": invite_result["failed"],
            }
            
        finally:
            await inviter.disconnect()

    async def execute_masslook(self) -> Dict:
        """
        Execute masslooking task.
        
        Returns:
            dict: {
                "processed": int,
                "success": int,
                "failed": int
            }
        """
        # Get userbot accounts for masslooking
        userbot_accounts = await self._get_userbot_accounts()
        
        if not userbot_accounts:
            raise ValueError("No userbot accounts available for masslooking")
        
        # Use first available account
        account = userbot_accounts[0]
        
        # Get session string
        from cryptography.fernet import Fernet
        encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")
        fernet = Fernet(encryption_key.encode())
        session_string = fernet.decrypt(account.session_string.encode()).decode()
        
        # Create masslooker
        masslooker = TelegramMasslooker(
            api_id=self.api_id,
            api_hash=self.api_hash,
            session_string=session_string,
        )
        
        try:
            await masslooker.connect()
            
            # Get masslook config
            config = self.task.config or {}
            stories_to_look = config.get("stories_to_look", 5)
            delay = config.get("delay_between_views_sec", 5)
            target_usernames = config.get("target_usernames", [])
            
            if not target_usernames:
                return {
                    "processed": 0,
                    "success": 0,
                    "failed": 0,
                    "message": "No target usernames specified in config",
                }
            
            # View stories
            result = await masslooker.view_stories(
                target_usernames=target_usernames,
                stories_to_look=stories_to_look,
                delay_between_views=delay,
            )
            
            return {
                "processed": len(target_usernames),
                "success": result["success"],
                "failed": result["failed"],
            }
            
        finally:
            await masslooker.disconnect()

    async def execute_comment(self) -> Dict:
        """
        Execute commenting task.
        
        Returns:
            dict: {
                "processed": int,
                "success": int,
                "failed": int
            }
        """
        if not self.task.target_chat_id:
            raise ValueError("target_chat_id is required for comment task")
        
        # Get userbot accounts for commenting
        userbot_accounts = await self._get_userbot_accounts()
        
        if not userbot_accounts:
            raise ValueError("No userbot accounts available for commenting")
        
        # Use first available account
        account = userbot_accounts[0]
        
        # Get session string
        from cryptography.fernet import Fernet
        encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")
        fernet = Fernet(encryption_key.encode())
        session_string = fernet.decrypt(account.session_string.encode()).decode()
        
        # Create commenter
        commenter = TelegramCommenter(
            api_id=self.api_id,
            api_hash=self.api_hash,
            session_string=session_string,
        )
        
        try:
            await commenter.connect()
            
            # Get comment config
            config = self.task.config or {}
            comment_text = config.get("comment_text", "Nice post!")
            comments_per_account = config.get("comments_per_account", 10)
            delay = config.get("delay_between_comments_sec", 60)
            
            # Comment on posts
            result = await commenter.comment_posts(
                target_chat_id=self.task.target_chat_id,
                comment_text=comment_text,
                max_comments=comments_per_account,
                delay_between_comments=delay,
            )
            
            return {
                "processed": comments_per_account,
                "success": result["success"],
                "failed": result["failed"],
            }
            
        finally:
            await commenter.disconnect()

    async def _get_userbot_accounts(self) -> list:
        """Get userbot accounts from userbot-service API."""
        import httpx
        
        userbot_service_url = os.getenv("USERBOT_SERVICE_URL", "http://userbot-service:8007")
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{userbot_service_url}/api/v1/userbot/accounts",
                    params={"project_id": self.task.project_id},
                    timeout=10.0,
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    accounts = data.get("data", [])
                    # Filter only active accounts with session
                    return [
                        acc for acc in accounts 
                        if acc.get("status") == "active" and acc.get("session_string")
                    ]
            except Exception as e:
                pass
        
        return []
