"""
Telegram bot handlers for moderation and funnels.
"""

import structlog
from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot import get_bot, get_dp
from app.services.content_client import content_service_client
from app.services.funnel_client import funnel_service_client

logger = structlog.get_logger()

# Get dispatcher
dp = get_dp()

if dp:
    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        """Handle /start command - trigger funnel."""
        # Get deep link parameter if exists
        args = message.text.split()
        trigger_value = args[1] if len(args) > 1 else "default"
        
        # Trigger funnel
        user_id = message.from_user.id
        result = await funnel_service_client.trigger_funnel(
            telegram_user_id=user_id,
            trigger_type="command",
            trigger_value=f"/start:{trigger_value}" if trigger_value != "default" else "/start",
        )
        
        if result and result.get("funnel_id"):
            # Funnel triggered - send first step message
            await message.answer(
                f"🎯 Добро пожаловать!\n\n"
                f"Запущена воронка: {result.get('funnel_name', 'N/A')}\n"
                f"Следите за сообщениями..."
            )
        else:
            # No funnel - send default welcome
            await message.answer(
                "👋 Привет! Я TeleFlow Bot.\n\n"
                "Доступные команды:\n"
                "/moderate — Очередь модерации\n"
                "/stats — Статистика\n"
                "/help — Помощь"
            )
        
        logger.info("user_started_bot", user_id=user_id, trigger=trigger_value)


    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        """Handle /help command."""
        await message.answer(
            "📖 **Помощь**\n\n"
            "/moderate — Показать очередь модерации\n"
            "/stats — Показать статистику\n"
            "/help — Эта справка"
        )


    @dp.message(Command("stats"))
    async def cmd_stats(message: types.Message):
        """Handle /stats command."""
        stats = await content_service_client.get_stats()
        if stats:
            await message.answer(
                f"📊 **Статистика**\n\n"
                f"📝 В очереди: {stats.get('pending', 0)}\n"
                f"✅ Одобрено: {stats.get('approved', 0)}\n"
                f"❌ Отклонено: {stats.get('rejected', 0)}\n"
                f"📤 Опубликовано: {stats.get('published', 0)}"
            )
        else:
            await message.answer("❌ Не удалось получить статистику")


    @dp.message(Command("moderate"))
    async def cmd_moderate(message: types.Message):
        """Handle /moderate command - show articles with inline keyboard."""
        queue_data = await content_service_client.get_moderation_queue(page=1, per_page=5)
        
        if not queue_data or not queue_data.get("items"):
            await message.answer("📭 Очередь пуста")
            return
        
        articles = queue_data["items"]
        total = queue_data.get("total", 0)
        
        # Send each article with inline keyboard
        for i, article in enumerate(articles, 1):
            title = article.get("title", "Без названия")[:100]
            priority = article.get("priority_score", 0)
            category = article.get("category", "N/A")
            source_id = article.get("source_id", "N/A")[:8]
            article_id = article.get("id")
            
            # Create inline keyboard
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✅ Одобрить",
                            callback_data=f"approve_{article_id}",
                        ),
                        InlineKeyboardButton(
                            text="❌ Отклонить",
                            callback_data=f"reject_{article_id}",
                        ),
                    ],
                ],
            )
            
            # Format message
            text = (
                f"📄 **Статья #{i}** ({priority} приоритет)\n\n"
                f"**{title}**\n\n"
                f"📁 Категория: {category}\n"
                f"📊 Источник: {source_id}\n"
                f"🔗 ID: `{article_id}`\n\n"
                f"Всего в очереди: {total}"
            )
            
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        
        # Add pagination if more articles
        pages = queue_data.get("pages", 1)
        if pages > 1:
            await message.answer(f"📄 Страница 1 из {pages}\n\nИспользуйте /moderate для обновления")


    @dp.callback_query(F.data.startswith("approve_"))
    async def callback_approve(callback: types.CallbackQuery):
        """Handle approve callback."""
        article_id = callback.data.split("_", 1)[1]
        
        success = await content_service_client.approve_article(article_id)
        
        if success:
            await callback.answer("✅ Статья одобрена", show_alert=True)
            logger.info("article_approved_via_bot", article_id=article_id, user_id=callback.from_user.id)
            
            # Delete the message
            try:
                await callback.message.delete()
            except:
                pass
        else:
            await callback.answer("❌ Ошибка при одобрении", show_alert=True)


    @dp.callback_query(F.data.startswith("reject_"))
    async def callback_reject(callback: types.CallbackQuery):
        """Handle reject callback."""
        article_id = callback.data.split("_", 1)[1]
        
        # For now, reject with default reason
        success = await content_service_client.reject_article(
            article_id,
            reason="rejected_via_bot",
            comment="Отклонено через Telegram бот",
        )
        
        if success:
            await callback.answer("❌ Статья отклонена", show_alert=True)
            logger.info("article_rejected_via_bot", article_id=article_id, user_id=callback.from_user.id)
            
            # Delete the message
            try:
                await callback.message.delete()
            except:
                pass
        else:
            await callback.answer("❌ Ошибка при отклонении", show_alert=True)
