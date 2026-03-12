# Celery Beat — Unified Scheduler

## Responsibility
Centralized task scheduling for all services.

## Configuration
Uses RedBeat (Redis-based scheduler) for distributed locking.

## Scheduled Tasks

| Task | Schedule | Service |
|------|----------|---------|
| fetch-all-sources | Every 5 min | content-service |
| apply-rules | Every 1 min | content-service |
| sync-meilisearch | Every 1 min | content-service |

## Queues

- content
- publishing
- funnel
- userbot
- promotion
- ai
- analytics
