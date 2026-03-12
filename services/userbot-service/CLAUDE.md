# Userbot Service — AI Context

## Responsibility
Userbots (Telegram client API), sessions, proxies, warming.

## Database: userbot_db
Tables: userbot_accounts, proxies, session_data

## Key Flows
1. Authorization: Send code → Verify → 2FA → Active
2. Warming: Day 1-7 gradual activity increase
3. Actions: Join, read, react, comment (via Telethon)

## Celery Tasks
- `warm_account(account_id)`
- `execute_userbot_action(action_type, params)`

## Dependencies
- Telethon for Telegram Client API
- Cryptography for session encryption
