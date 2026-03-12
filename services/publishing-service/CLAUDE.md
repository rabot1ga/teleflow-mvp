# Publishing Service — AI Context

## Responsibility
Publishing, templates, scheduling, content calendar.

## Database: publish_db
Tables: publish_targets, publish_templates, publish_jobs

## Key Flows
1. Publishing: Validate → Rate Check → Template → Render → Send → Save

## Events Published
- `article.published` {article_id, target_id, message_id}

## Events Consumed
- `article.approved` {article_id, target_id, schedule_at}

## Celery Tasks
- `publish_article(article_id, target_id)`
- `check_scheduled_jobs()`
