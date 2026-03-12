# Promotion Service — AI Context

## Responsibility
Parsing, inviting, masslooking, commenting.

## Database: promo_db
Tables: promotion_tasks, parsed_users

## Key Flows
1. Parsing: Target groups → Fetch members → Store
2. Inviting: Parsed users → Invite (via userbot) → Stats
3. Masslooking: Stories → Views (via userbot)

## Celery Tasks
- `parse_users(task_id)`
- `invite_users(task_id)`
- `masslook(task_id)`
