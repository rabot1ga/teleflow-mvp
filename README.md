# ⚡ TeleFlow Platform

**Modern Telegram Operations Management Platform**

[![Status](https://img.shields.io/badge/status-production--ready-success)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 📖 О проекте

**TeleFlow Platform** — модульная платформа для автоматизации работы с Telegram-каналами.

| Модуль | Назначение | Статус |
|--------|------------|--------|
| **Content Hub** | Агрегация контента из RSS, API, парсинг | ✅ Production |
| **Модерация** | Ручная и автоматическая модерация | ✅ Production |
| **Публикация** | Планирование и публикация в Telegram | ✅ Production |
| **Воронки** | Создание воронок, лид-магниты, CRM | ✅ Production |
| **Рассылки** | Массовые рассылки по базе | ✅ Production |
| **Telegram Бот** | Управление через Telegram | ✅ Production |
| **Юзерботы** | Управление аккаунтами | ⏸️ Development |
| **Продвижение** | Парсинг, инвайтинг, масслукинг | ⏸️ Development |
| **AI** | AI-обработка контента | ⏸️ Development |
| **Аналитика** | Дашборды, статистика | ⏸️ Development |

---

## 🚀 Быстрый старт

### 1. Запуск

```bash
# Клонировать
git clone https://github.com/rabot1ga/teleflow-mvp.git
cd teleflow-mvp

# Запустить
docker compose up -d

# Миграции
docker compose exec auth-service alembic upgrade head
docker compose exec content-service alembic upgrade head
docker compose exec publishing-service alembic upgrade head
docker compose exec funnel-service alembic upgrade head
```

### 2. Доступ

| Сервис | URL |
|--------|-----|
| **Frontend** | http://localhost:3000 |
| **Grafana** | http://localhost:3001 (admin/admin) |
| **Prometheus** | http://localhost:9090 |

### 3. Первый вход

1. http://localhost:3000/register
2. Register с вашим email
3. Login
4. Создать проект через API или UI

---

## 🏗 Архитектура

```
┌─────────────┐
│   Traefik   │ :80/:443
│ API Gateway │
└──────┬──────┘
       │
 ┌─────┴─────┬──────────┬──────────┐
 │           │          │          │
Frontend   Auth     Content   Funnel
:3000     :8001     :8002     :8005
```

### Сервисы

| Сервис | Порт | Статус |
|--------|------|--------|
| Auth Service | 8001 | ✅ |
| Content Service | 8002 | ✅ |
| Publishing Service | 8004 | ✅ |
| Funnel Service | 8005 | ✅ |
| Bot Gateway | 8006 | ✅ |
| Frontend | 3000 | ✅ |

### Инфраструктура

| Сервис | Назначение |
|--------|------------|
| PostgreSQL (9 БД) | Базы данных |
| Redis | Cache, broker, Pub/Sub |
| Meilisearch | Поиск |
| MinIO | Файлы |
| Prometheus | Метрики |
| Grafana | Дашборды |
| Loki | Логи |

---

## 🔌 API

### Auth

```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John"
}

# Login
POST /api/v1/auth/login
```

### Content

```bash
# Sources
GET /api/v1/content/sources?project_id={id}
POST /api/v1/content/sources

# Articles
GET /api/v1/content/articles?project_id={id}

# Moderation
GET /api/v1/content/moderation/queue
POST /api/v1/content/articles/{id}/approve
```

### Funnels

```bash
# Funnels
GET /api/v1/funnels/funnels?project_id={id}
POST /api/v1/funnels/funnels

# Broadcasts
POST /api/v1/funnels/broadcasts/{id}/start
```

**Full API docs:** http://localhost:8001/docs

---

## 🤖 Telegram Бот

### Настройка

1. Создать бота через @BotFather
2. Получить токен
3. Добавить в `.env`:

```bash
TELEGRAM_BOT_TOKEN=123456:ABCdefGHIjklMNOpqrs
```

4. Перезапустить:

```bash
docker compose restart bot-gateway
```

### Команды

```
/start - Запустить
/help - Справка
/stats - Статистика
/moderate - Модерация
```

---

## 📊 Мониторинг

### Grafana

http://localhost:3001 (admin/admin)

**Дашборды:**
- Service Health
- Request Rate & Latency
- Error Rates
- Celery Queue
- Business Metrics

### Prometheus

http://localhost:9090

**Метрики:**
- `http_requests_total`
- `http_request_duration_seconds`
- `celery_tasks_total`
- `articles_created_total`

---

## 💻 Разработка

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd services/auth-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Миграции

```bash
docker exec auth-service alembic upgrade head
```

### Тесты

```bash
python3 e2e_test.py
python3 e2e_funnel_test.py
python3 e2e_broadcast_test.py
```

---

## 📁 Структура

```
teleflow/
├── frontend/              # React SPA
├── services/
│   ├── auth-service/     # Auth, RBAC
│   ├── content-service/  # Content, moderation
│   ├── publishing-service/ # Publishing
│   ├── funnel-service/   # Funnels, broadcasts
│   └── bot-gateway/      # Telegram bot
├── shared/
│   └── teleflow-common/  # Shared library
├── infra/                # Infrastructure
└── docker-compose.yml
```

---

## 📚 Документация

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) — Полное руководство
- [QUICKSTART.md](QUICKSTART.md) — Быстрый старт
- [API Docs](http://localhost:8001/docs) — Swagger

---

## 🛠 Стек

**Frontend:**
- React 18, Vite, TypeScript
- Zustand, TanStack Query
- Recharts

**Backend:**
- Python 3.11, FastAPI
- SQLAlchemy 2.0, Pydantic v2
- Celery, Redis

**Infrastructure:**
- PostgreSQL, Redis
- Traefik, Prometheus, Grafana
- Meilisearch, MinIO

---

## 📞 Контакты

- **GitHub:** https://github.com/rabot1ga/teleflow-mvp
- **Issues:** https://github.com/rabot1ga/teleflow-mvp/issues

---

## 📄 License

MIT License

---

*TeleFlow Platform v1.0.0 — Production Ready 🚀*
