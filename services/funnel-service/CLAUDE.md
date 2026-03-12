# Funnel Service — AI Context

## Responsibility
Funnels, lead magnets, broadcasts, CRM.

## Database: funnel_db
Tables: funnels, funnel_steps, funnel_users, lead_magnets, broadcasts

## Key Flows
1. Funnel: Trigger → Step 1 → Delay → Step 2 → ... → Complete
2. Broadcast: Create → Schedule → Execute (batched) → Stats

## Events Published
- `funnel.user_entered` {funnel_id, user_id, source}
- `funnel.step_completed` {funnel_id, step_id, user_id}
- `funnel.completed` {funnel_id, user_id}

## Events Consumed
- `user.started_bot` {user_id, deep_link_param}
- `user.callback` {user_id, callback_data}

## Celery Tasks
- `process_funnel_step(user_id, step_id)`
- `check_pending_steps()`
- `execute_broadcast(broadcast_id)`
