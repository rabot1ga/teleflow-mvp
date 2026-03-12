# Content Service — AI Context

## Responsibility

Manages content sources, article ingestion, deduplication, enrichment, and moderation.

## Database: content_db

### Tables

- `sources` — Content sources (RSS, API, scraper, webhook, telegram)
- `source_runs` — Source fetch history
- `articles` — Articles/materials
- `article_versions` — Article edit history
- `automation_rules` — Rules for auto-moderation
- `moderation_batches` — Batch moderation groups

## Key Flows

1. **Ingestion**: Source → Fetch → Parse → Dedup → Enrich → Rules → Save
2. **Moderation**: Queue → Approve/Reject/Edit → Publish event
3. **Rules Engine**: Conditions → Actions (auto_approve, auto_reject, set_priority, etc.)

## API Endpoints

```
GET    /api/v1/content/sources                    — список
POST   /api/v1/content/sources                    — создать
GET    /api/v1/content/articles                   — список
POST   /api/v1/content/articles/{id}/approve      — одобрить
POST   /api/v1/content/articles/{id}/reject       — отклонить
```

## Events Published

- `article.created` {article_id, source_id, category}
- `article.approved` {article_id, target_id, schedule_at}
- `article.rejected` {article_id, reason}

## Events Consumed

- `article.published` {article_id, message_id} — update article status

## Dependencies

- PostgreSQL (content_db)
- Redis (cache + broker)
- Meilisearch (search)
- MinIO (file storage)
- ai-service (HTTP) — AI operations
- bot-gateway (HTTP) — Telegram notifications

## Celery Tasks

- `fetch_source(source_id)` — fetch single source
- `fetch_all_sources()` — beat task, every 5 min
- `apply_rules(article_id)` — apply automation rules
- `sync_meilisearch(article_id)` — update search index
