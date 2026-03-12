"""
Bot Gateway — Telegram Bot integration.
"""

from typing import Optional

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings

logger = structlog.get_logger()

# Bot instance (created lazily)
_bot: Optional[Bot] = None
_dp: Optional[Dispatcher] = None


def get_bot() -> Optional[Bot]:
    """Get bot instance if token is configured."""
    global _bot, _dp
    if _bot is None and settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_BOT_TOKEN != "your-telegram-bot-token-here":
        try:
            _bot = Bot(
                token=settings.TELEGRAM_BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )
            _dp = Dispatcher(storage=MemoryStorage())
            logger.info("bot_initialized")
        except Exception as e:
            logger.error("bot_init_failed", error=str(e))
            return None
    return _bot


def get_dp() -> Optional[Dispatcher]:
    """Get dispatcher instance."""
    get_bot()  # Ensure bot is initialized
    return _dp


async def start_bot():
    """Start bot polling."""
    bot = get_bot()
    if bot:
        dp = get_dp()
        await dp.start_polling(bot)


async def stop_bot():
    """Stop bot."""
    bot = get_bot()
    if bot:
        await bot.session.close()
    dp = get_dp()
    if dp:
        await dp.storage.close()
