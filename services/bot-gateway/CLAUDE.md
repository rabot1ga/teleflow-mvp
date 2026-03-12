# Bot Gateway — AI Context

## Responsibility
Telegram Bot API, webhooks, message routing, notifications.

## Database: bot_db
Tables: bot_sessions, webhook_logs, notification_queue

## Key Flows
1. Webhook: Telegram → Webhook → Route → Service
2. Send: Service → Internal API → Telegram Bot API

## API Endpoints (Internal)
- POST /internal/bot/send-message
- POST /internal/bot/send-photo
- POST /internal/bot/check-subscription

## Events Published
- `user.subscribed` {user_id, channel_id}
- `user.started_bot` {user_id, deep_link_param}
- `user.callback` {user_id, callback_data}

## Dependencies
- aiogram 3.x for Telegram Bot API
