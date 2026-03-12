# Analytics Service — AI Context

## Responsibility
Statistics, reports, dashboards.

## Database: analytics_db
Tables: analytics_events, analytics_daily

## Key Flows
1. Event ingestion: Events from all services → Store → Aggregate
2. Aggregation: Daily stats → Store
3. Reports: Query → Aggregate → Return

## Events Consumed
- `article.created`, `article.approved`, `article.published`
- `funnel.user_entered`, `funnel.step_completed`, `funnel.completed`
- `user.subscribed`, `user.started_bot`
- `promotion.task_completed`

## Celery Tasks
- `aggregate_daily_stats(project_id, date)`
- `process_event(event_type, payload)`
