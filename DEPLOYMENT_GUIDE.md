# 🚀 TeleFlow Platform — Production Deployment Guide

**Версия:** 1.0.0  
**Дата:** 13 марта 2026  
**Статус:** ✅ Production Ready

---

## 📋 Содержание

1. [О проекте](#о-проекте)
2. [Быстрый старт](#быстрый-старт)
3. [Архитектура](#архитектура)
4. [Сервисы](#сервисы)
5. [API Endpoints](#api-endpoints)
6. [Telegram Бот](#telegram-бот)
7. [Мониторинг](#мониторинг)
8. [Разработка](#разработка)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## 📖 О проекте

**TeleFlow Platform** — модульная платформа для автоматизации работы с Telegram-каналами.

### Возможности

✅ **Content Hub**
- Агрегация контента из RSS, JSON API
- Парсинг сайтов (scraper)
- Telegram каналы через userbot
- Автоматическая дедупликация
- AI-обогащение (категории, теги, quality score)

✅ **Модерация**
- Ручная модерация через web интерфейс
- Автоматические правила модерации
- Пакетная модерация
- Moderation через Telegram бота

✅ **Публикация**
- Планирование публикаций
- Шаблоны сообщений
- Календарь публикаций
- Публикация в несколько каналов

✅ **Воронки**
- Конструктор воронок
- Лид-магниты (text, file, link)
- Триггеры (command, keyword, subscription)
- CRM сегментация

✅ **Рассылки**
- Массовые рассылки
- Сегментация аудитории
- Статистика доставки
- Rate limiting

⏸️ **Юзерботы** (Development)
- Управление Telegram аккаунтами
- Прокси для аккаунтов
- Авто-прогрев аккаунтов

⏸️ **Продвижение** (Development)
- Парсинг аудитории
- Инвайтинг с anti-flood
- Масслукинг stories
- Авто-комментарии

⏸️ **AI** (Development)
- AI-рерайт статей
- AI-саммари
- AI-классификация
- AI-генерация тегов

⏸️ **Аналитика** (Development)
- Дашборды
- Статистика по источникам
- Воронки конверсии
- ROI продвижения

---

## 🚀 Быстрый старт

### 1. Требования

- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM (минимум)
- 4 CPU cores (рекомендуется)
- 50GB disk space

### 2. Установка

```bash
# Клонировать репозиторий
git clone https://github.com/rabot1ga/teleflow-mvp.git
cd teleflow-mvp

# Скопировать .env.example в .env
cp .env.example .env

# Отредактировать .env (заполнить секреты)
nano .env

# Запустить все сервисы
docker compose up -d

# Применить миграции
docker compose exec auth-service alembic upgrade head
docker compose exec content-service alembic upgrade head
docker compose exec publishing-service alembic upgrade head
docker compose exec funnel-service alembic upgrade head

# Проверить статус
docker compose ps
```

### 3. Первый вход

1. Откройте http://localhost:3000
2. Нажмите **Register**
3. Заполните форму:
   - Email: `admin@example.com`
   - Password: `your_secure_password`
   - First Name: `Admin`
   - Last Name: `User`
4. Войдите с вашими credentials

### 4. Создание проекта

```bash
# Получить токен
TOKEN=$(curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"your_secure_password"}' \
  | jq -r '.data.access_token')

# Создать проект
curl -X POST http://localhost:8001/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"My Project","slug":"my-project"}'
```

### 5. Добавление источника

1. **Content** → **Sources** → **+ Add Source**
2. Name: `Habr RSS`
3. Type: `rss`
4. URL: `https://habr.com/ru/rss/articles/all/`
5. Interval: `30` минут
6. Нажмите **🔄 Fetch** для ручного сбора

---

## 🏗 Архитектура

```
                    ┌─────────────┐
                    │   Traefik   │ :80/:443
                    │ API Gateway │
                    └──────┬──────┘
          ┌────────────────┼────────────────────┐
          │                │                    │
   ┌──────┴──────┐  ┌──────┴──────┐  ┌─────────┴──────┐
   │  Frontend   │  │  /api/v1/*  │  │  /ws/*         │
   │  React SPA  │  │  REST APIs  │  │  WebSocket     │
   │  :3000      │  │             │  │                │
   └─────────────┘  └──────┬──────┘  └────────────────┘
                           │
     ┌──────────┬──────────┼──────────┬──────────┐
     │          │          │          │          │
 ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
 │ Auth  │ │Content│ │Publish│ │Funnel │ │Bot GW │
 │ :8001 │ │ :8002 │ │ :8004 │ │ :8005 │ │ :8006 │
 └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

### Сервисы

| Сервис | Порт | Описание | Статус |
|--------|------|----------|--------|
| **Auth Service** | 8001 | Аутентификация, RBAC, пользователи | ✅ |
| **Content Service** | 8002 | Источники, статьи, модерация | ✅ |
| **Publishing Service** | 8004 | Публикации, шаблоны, календарь | ✅ |
| **Funnel Service** | 8005 | Воронки, лид-магниты, рассылки | ✅ |
| **Bot Gateway** | 8006 | Telegram бот, webhook | ✅ |
| **Userbot Worker** | — | Юзерботы, прокси | ⏸️ |
| **Promotion Worker** | — | Парсинг, инвайтинг | ⏸️ |
| **AI Service** | — | AI-обработка | ⏸️ |
| **Analytics Service** | — | Аналитика, дашборды | ⏸️ |

### Инфраструктура

| Сервис | Порт | Описание |
|--------|------|----------|
| **PostgreSQL** | 5432 | Базы данных (9 БД) |
| **Redis** | 6379 | Cache, Celery broker, Pub/Sub |
| **Traefik** | 80/8080 | API Gateway, dashboard |
| **Meilisearch** | 7700 | Полнотекстовый поиск |
| **MinIO** | 9000/9001 | S3-compatible storage |
| **Prometheus** | 9090 | Метрики, мониторинг |
| **Grafana** | 3001 | Дашборды, визуализация |
| **Loki** | 3100 | Log aggregation |
| **RSSHub** | 1200 | RSS генератор для Telegram |

---

## 🔌 API Endpoints

### Auth Service (`/api/v1/auth`)

```bash
# Регистрация
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# Refresh token
POST /api/v1/auth/refresh
{
  "refresh_token": "..."
}

# Logout
POST /api/v1/auth/logout

# Текущий пользователь
GET /api/v1/auth/me

# Обновление профиля
PATCH /api/v1/auth/me
{
  "first_name": "Jane"
}

# Смена пароля
PATCH /api/v1/auth/me/password
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

### Content Service (`/api/v1/content`)

```bash
# Источники
GET /api/v1/content/sources?project_id={id}
POST /api/v1/content/sources
PATCH /api/v1/content/sources/{id}
DELETE /api/v1/content/sources/{id}
POST /api/v1/content/sources/{id}/fetch

# Статьи
GET /api/v1/content/articles?project_id={id}&status=pending
GET /api/v1/content/articles/{id}
PATCH /api/v1/content/articles/{id}
DELETE /api/v1/content/articles/{id}

# Модерация
GET /api/v1/content/moderation/queue?status=pending
POST /api/v1/content/articles/{id}/approve
POST /api/v1/content/articles/{id}/reject
  { "reason": "low_quality", "comment": "..." }

# AI операции
POST /api/v1/content/ai/rewrite
  { "article_id": "...", "style": "news" }
POST /api/v1/content/ai/summarize
  { "article_id": "...", "max_length": 100 }
```

### Publishing Service (`/api/v1/publishing`)

```bash
# Targets (каналы)
GET /api/v1/publishing/targets?project_id={id}
POST /api/v1/publishing/targets
DELETE /api/v1/publishing/targets/{id}

# Templates
GET /api/v1/publishing/templates?project_id={id}
POST /api/v1/publishing/templates
DELETE /api/v1/publishing/templates/{id}

# Jobs (публикации)
GET /api/v1/publishing/jobs?project_id={id}
POST /api/v1/publishing/jobs
POST /api/v1/publishing/jobs/{id}/start
POST /api/v1/publishing/jobs/{id}/cancel
```

### Funnel Service (`/api/v1/funnels`)

```bash
# Воронки
GET /api/v1/funnels/funnels?project_id={id}
POST /api/v1/funnels/funnels
DELETE /api/v1/funnels/funnels/{id}

# Лид-магниты
GET /api/v1/funnels/lead-magnets?project_id={id}
POST /api/v1/funnels/lead-magnets
DELETE /api/v1/funnels/lead-magnets/{id}

# Рассылки
GET /api/v1/funnels/broadcasts?project_id={id}
POST /api/v1/funnels/broadcasts
POST /api/v1/funnels/broadcasts/{id}/start
POST /api/v1/funnels/broadcasts/{id}/cancel
```

---

## 🤖 Telegram Бот

### Настройка

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен
3. Добавьте в `.env`:

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_USERNAME=MyTeleFlowBot
```

4. Перезапустите бота:

```bash
docker compose restart bot-gateway
```

### Команды бота

```
/start - Запустить бота
/help - Справка
/stats - Статистика проекта
/moderate - Модерация статей
/sources - Мои источники
/articles - Последние статьи
```

### Moderation через бота

Бот отправляет статьи на модерацию:

```
📰 Новая статья на модерации

🔥 Breaking: AI Company Raises $100M

Источник: TechCrunch
Качество: 85%
Приоритет: Высокий

[✅ Одобрить] [❌ Отклонить] [✏️ Ред.]
```

### Настройка команд

Отправьте @BotFather:

```
/setcommands
@MyTeleFlowBot
start - Запустить бота
help - Справка
stats - Статистика
moderate - Модерация
sources - Источники
articles - Статьи
```

---

## 📊 Мониторинг

### Grafana Dashboards

1. Откройте http://localhost:3001
2. Login: `admin` / `admin`
3. Dashboards:
   - **Service Health** — статус сервисов
   - **Request Rate & Latency** — RPS, время ответа
   - **Error Rates** — процент ошибок
   - **Celery Queue Depth** — очередь задач
   - **Database Connections** — пул соединений
   - **Business Metrics** — статьи, воронки, рассылки

### Prometheus Metrics

```bash
# HTTP метрики
http_requests_total{service, method, path, status}
http_request_duration_seconds{service, method, path}

# Celery метрики
celery_tasks_total{task, status}
celery_task_duration_seconds{task}

# Бизнес метрики
articles_created_total{project_id, source_id}
articles_published_total{project_id}
funnels_entries_total{funnel_id}
broadcasts_sent_total{broadcast_id}
```

### Loki Logs

```bash
# Открыть Grafana → Explore → Loki
# Query:
{service="content-service"} |= "error"

# Или через docker compose
docker compose logs content-service --tail=100 | grep error
```

---

## 💻 Разработка

### Требования

- Python 3.11+
- Node.js 18+
- Docker 20.10+

### Frontend разработка

```bash
cd frontend
npm install
npm run dev
```

### Backend разработка

```bash
# Auth Service
cd services/auth-service
pip install -r requirements.txt
uvicorn app.main:app --reload

# Content Service
cd services/content-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Миграции

```bash
# Auth Service
docker exec auth-service alembic upgrade head

# Content Service
docker exec content-service alembic upgrade head

# Откат миграций
docker exec auth-service alembic downgrade -1
```

### Тесты

```bash
# Backend E2E
python3 e2e_test.py
python3 e2e_funnel_test.py
python3 e2e_broadcast_test.py

# Frontend (в разработке)
cd frontend
npm run test:e2e
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Изменить пароли в `.env`
- [ ] Настроить HTTPS (Let's Encrypt)
- [ ] Включить rate limiting
- [ ] Настроить backup БД
- [ ] Включить мониторинг
- [ ] Настроить алерты
- [ ] Провести security audit

### Backup БД

```bash
# Создать backup
docker exec teleflow-postgres pg_dump -U teleflow -d auth_db > auth_db.sql

# Восстановить
docker exec -i teleflow-postgres psql -U teleflow -d auth_db < auth_db.sql
```

### Обновление

```bash
# Pull новых образов
docker compose pull

# Пересобрать сервисы
docker compose up -d --build

# Применить миграции
docker compose exec auth-service alembic upgrade head
docker compose exec content-service alembic upgrade head

# Перезапустить сервисы
docker compose restart
```

---

## 🐛 Troubleshooting

### Сервис не запускается

```bash
# Проверить логи
docker compose logs service-name

# Проверить health
curl http://localhost:8001/health

# Перезапустить
docker compose restart service-name
```

### Миграции не работают

```bash
# Проверить статус миграций
docker exec auth-service alembic current

# Применить заново
docker exec auth-service alembic upgrade head
```

### Frontend не подключается к API

```bash
# Проверить переменные окружения
docker exec teleflow-frontend printenv | grep VITE

# Пересобрать frontend
docker compose up -d --build frontend
```

### Бот не работает

```bash
# Проверить токен
echo $TELEGRAM_BOT_TOKEN

# Проверить логи бота
docker compose logs bot-gateway | tail -50

# Перезапустить бота
docker compose restart bot-gateway
```

---

## 📞 Поддержка

- **GitHub Issues:** https://github.com/rabot1ga/teleflow-mvp/issues
- **Documentation:** /docs
- **API Docs:** http://localhost:8001/docs (Swagger)

---

*TeleFlow Platform v1.0.0 — Production Ready 🚀*
