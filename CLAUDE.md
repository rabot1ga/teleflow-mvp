# TeleFlow Platform — AI Context

## Architecture

- **9 microservices** + API Gateway (Traefik) + Frontend (React SPA)
- **Database-per-service**: PostgreSQL 16 (отдельная БД для каждого сервиса)
- **Async tasks**: Celery 5.x + Redis 7+ broker
- **Events**: Redis Pub/Sub для асинхронного взаимодействия
- **Search**: Meilisearch для полнотекстового поиска
- **Files**: MinIO (S3-compatible storage)

## Tech Stack

| Layer | Technology |
|-------|------------|
| **API Gateway** | Traefik 2.x (routing, TLS, rate limiting, CORS) |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async) |
| **Frontend** | React 18+, Vite, TypeScript, Zustand, TanStack Query |
| **Telegram Bot** | aiogram 3.x |
| **Telegram Userbot** | Telethon |
| **Database** | PostgreSQL 16 |
| **Cache/Broker** | Redis 7+ |
| **Task Queue** | Celery 5.x + Celery Beat |
| **Search** | Meilisearch |
| **Files** | MinIO |
| **Monitoring** | Prometheus + Grafana + Loki |
| **Containers** | Docker, Docker Compose |

## Project Structure

```
teleflow/
├── docker-compose.yml          # Main orchestration
├── docker-compose.override.yml # Development overrides
├── .env.example                # Environment template
├── Makefile                    # Development commands
├── CLAUDE.md                   # This file
├── README.md                   # Project overview
├── WORK.md                     # Development progress tracker
│
├── shared/
│   └── teleflow-common/        # Shared Python package
│       ├── teleflow_common/
│       │   ├── __init__.py
│       │   ├── auth/           # JWT, RBAC, FastAPI dependencies
│       │   ├── schemas/        # Response schemas (StandardResponse, etc.)
│       │   ├── middleware/     # CorrelationID, logging, error handler
│       │   ├── clients/        # BaseServiceClient, EventBus
│       │   ├── database/       # Base model, mixins, session factory
│       │   └── config/         # BaseSettings
│       ├── pyproject.toml
│       └── README.md
│
├── services/
│   ├── auth-service/           # Port 8001, auth_db
│   ├── content-service/        # Port 8002, content_db
│   ├── publishing-service/     # Port 8004, publish_db
│   ├── funnel-service/         # Port 8005, funnel_db
│   ├── bot-gateway/            # Port 8006, bot_db
│   ├── userbot-service/        # Port 8007, userbot_db
│   ├── promotion-service/      # Port 8008, promo_db
│   ├── ai-service/             # Port 8009, no DB
│   └── analytics-service/      # Port 8010, analytics_db
│
├── frontend/                   # React SPA, port 3000
│
└── infra/
    ├── traefik/                # API Gateway config
    ├── prometheus/             # Metrics scraping config
    └── grafana/                # Dashboards provisioning
```

## Services Overview

| # | Service | Port | Database | Celery Worker | Responsibility |
|---|---------|------|----------|---------------|----------------|
| 1 | api-gateway (Traefik) | 80/443 | — | — | Routing, CORS, rate limit, TLS |
| 2 | auth-service | 8001 | auth_db | — | Authentication, JWT, RBAC, users, projects |
| 3 | content-service | 8002 | content_db | ✅ | Sources, ingestion, dedup, moderation, rules |
| 4 | publishing-service | 8004 | publish_db | ✅ | Publishing, templates, scheduling, calendar |
| 5 | funnel-service | 8005 | funnel_db | ✅ | Funnels, lead magnets, broadcasts, CRM |
| 6 | bot-gateway | 8006 | bot_db | — | Telegram Bot API, webhooks, routing |
| 7 | userbot-service | 8007 | userbot_db | ✅ | Userbots, sessions, proxies, warming |
| 8 | promotion-service | 8008 | promo_db | ✅ | Parsing, inviting, masslooking, commenting |
| 9 | ai-service | 8009 | — | ✅ | LLM operations (rewrite, summarize, classify) |
| 10 | analytics-service | 8010 | analytics_db | ✅ | Statistics, reports, dashboards |
| 11 | frontend | 3000 | — | — | React SPA |

## Conventions

### API Response Format

All APIs return `StandardResponse`:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO8601"
  }
}
```

Error format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [...]
  },
  "meta": { "request_id": "uuid" }
}
```

### Pagination

- **Cursor-based** для больших списков (articles, users)
- **Offset/limit** для admin интерфейсов

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "per_page": 20,
    "pages": 8
  }
}
```

### Database

- Все модели наследуются от `TimestampMixin` (created_at, updated_at)
- Alembic для миграций
- Database-per-service: сервис **не** ходит в чужую БД — только через HTTP API

### Inter-service Communication

**Sync (HTTP):**
- Через `BaseServiceClient` (shared/teleflow-common/clients/base.py)
- Автоматически: retry (3x), timeout (30s), correlation_id propagation

**Async (Events via Redis Pub/Sub):**
- Через `EventBus` (shared/teleflow-common/clients/event_bus.py)
- Event Catalog описан в tz.md

### Bot Operations

**ВАЖНО:** Другие сервисы **не** вызывают Telegram API напрямую — только через bot-gateway:

```python
# POST /internal/bot/send-message
{
    "chat_id": 123456,
    "text": "Hello",
    "parse_mode": "HTML"
}
```

### Logging

- Structured logging (JSON) во всех сервисах
- Correlation ID (`X-Request-ID`) для трассировки между сервисами
- Fields: timestamp, level, service, request_id, user_id, message, duration_ms

### Error Handling

- `ErrorHandler` middleware ловит все исключения
- Возвращает стандартизированный ErrorResponse
- Логирует стектрейс в JSON формате

## Running Commands

```bash
# Start all services
make up

# Start with rebuild
make up-build

# View logs
make logs

# Run migrations
make migrate

# Run tests
make test

# Lint code
make lint

# Stop all
make down

# Shell in service
make shell SERVICE=auth-service

# Connect to DB
make db
```

## Development Workflow

1. **Shared library first** — не начинать сервисы пока `teleflow-common` не готов
2. **One service at a time** — завершить сервис до MVP, потом переходить к следующему
3. **Tests immediately** — писать тесты вместе с кодом
4. **Update CLAUDE.md** — после каждого этапа обновлять контекст

## Event Catalog (Key Events)

| Event | Publisher | Consumers | Payload |
|-------|-----------|-----------|---------|
| `article.created` | content | analytics | article_id, source_id, category |
| `article.approved` | content | publishing, analytics | article_id, target_id, schedule_at |
| `article.published` | publishing | content, analytics | article_id, target_id, message_id |
| `funnel.user_entered` | funnel | analytics | funnel_id, user_id, source |
| `user.subscribed` | bot-gateway | funnel, analytics | user_id, channel_id |

## Key Design Decisions

1. **No separate scheduler-service** — Celery Beat внутри каждого сервиса
2. **No separate notification-service** — модуль в bot-gateway
3. **No separate moderation-service** — объединён с content-service
4. **Traefik as API Gateway** — единая точка входа, rate limiting, CORS
5. **Database-per-service** — для простоты разработки одна PostgreSQL инстанция, разные БД

## MCP Usage Guidelines

| MCP | When to Use |
|-----|-------------|
| **filesystem** | Always — primary tool for code operations |
| **postgres** | Designing schemas, checking migrations, debug queries |
| **sequential-thinking** | Complex architectural decisions, Rules/Funnel/Publishing Engine design |
| **context7** | Looking up aiogram 3, SQLAlchemy 2.0 async, Telethon, FastAPI APIs |

## Prompt Template for Creating Services

```
Создай {service-name} для TeleFlow Platform.

Контекст: прочитай CLAUDE.md в корне проекта и
в services/{service-name}/CLAUDE.md (если есть)

Структура сервиса:
services/{service-name}/
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── api/v1/          # Routers
│   ├── services/        # Business logic
│   ├── tasks/           # Celery tasks
│   └── events/          # Event handlers
├── alembic/
├── tests/
├── Dockerfile
├── requirements.txt
└── CLAUDE.md

Начни с: {конкретная задача этого этапа}
```

## Related Documents

- [tz.md](./tz.md) — Полное техническое задание
- [WORK.md](./WORK.md) — План разработки и прогресс
