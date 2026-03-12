# 🚀 TeleFlow Platform

**Модульная платформа для полного цикла работы с Telegram-каналами**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/rabot1ga/teleflow-mvp)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose-v2-blue.svg)](https://docs.docker.com/compose/)
[![Status](https://img.shields.io/badge/status-MVP%20ready-brightgreen)](https://github.com/rabot1ga/teleflow-mvp)

---

## 📋 О проекте

**TeleFlow** — микросервисная платформа для автоматизации Telegram-каналов:

| Модуль | Описание |
|--------|----------|
| 📰 **Content Hub** | Агрегация из RSS, API, парсинг + модерация |
| 📤 **Publishing** | Планирование и публикация в каналы |
| 🎯 **Funnels** | Воронки, лид-магниты, рассылки |
| 🤖 **Userbots** | Управление Telegram аккаунтами |
| 📈 **Promotion** | Парсинг, инвайтинг, масслукинг |
| 🧠 **AI** | AI-обработка контента |
| 📊 **Analytics** | Дашборды и статистика |
| 🔗 **RSSHub** | RSS для Telegram и соцсетей |

---

## ⚡ Быстрый старт

```bash
# 1. Клонирование
git clone https://github.com/rabot1ga/teleflow-mvp.git
cd teleflow

# 2. Настройка
cp .env.example .env

# 3. Запуск
docker compose up -d
make migrate

# 4. Frontend
cd frontend && npm install && npm run dev
```

**Готово!** 🎉

- Frontend: http://localhost:3000
- Login: `demo@example.com` / `Demo123!`

---

## 🏗 Архитектура

```
                    ┌─────────────┐
                    │   Traefik   │ :80/443
                    │ API Gateway │
                    └──────┬──────┘
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────┴──────┐  ┌──────┴──────┐  ┌────┴────┐
   │  Frontend   │  │  REST APIs  │  │   WS    │
   │  React SPA  │  │  9 services │  │ Gateway │
   │  :3000      │  │             │  │         │
   └─────────────┘  └──────┬──────┘  └─────────┘
                           │
    ┌──────────┬───────────┼───────────┬──────────┐
    │          │           │           │          │
┌───┴───┐ ┌───┴───┐ ┌────┴────┐ ┌────┴────┐ ┌───┴────┐
│ Auth  │ │Content│ │Publish  │ │ Funnel  │ │ Userbot│
│ :8001 │ │ :8002 │ │ :8004   │ │ :8005   │ │ :8007  │
└───────┘ └───────┘ └─────────┘ └─────────┘ └────────┘
    │          │           │           │          │
┌───┴───┐ ┌───┴───┐ ┌────┴────┐ ┌────┴────┐ ┌───┴────┐
│ Bot   │ │Promo  │ │   AI    │ │Analytics│ │ Celery │
│ :8006 │ │ :8008 │ │ :8009   │ │ :8010   │ │ Beat   │
└───────┘ └───────┘ └─────────┘ └─────────┘ └────────┘
```

---

## 🛠 Стек

| Слой | Технологии |
|------|------------|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, Celery 5.x |
| **Frontend** | React 18, TypeScript, Vite, Zustand, TanStack Query |
| **Базы данных** | PostgreSQL 16 (9 БД), Redis 7 |
| **Инфраструктура** | Docker, Traefik, Prometheus, Grafana, Loki |
| **Telegram** | aiogram 3.x (Bot), Telethon (Userbot) |
| **Поиск** | Meilisearch |
| **Файлы** | MinIO (S3-compatible) |

---

## 📊 Статус

| Сервис | Порт | Статус |
|--------|------|--------|
| Auth | 8001 | ✅ 100% |
| Content | 8002 | ✅ 100% |
| Publishing | 8004 | ✅ 100% |
| Funnels | 8005 | ✅ 100% |
| Bot Gateway | 8006 | ✅ 100% |
| Userbot | 8007 | ✅ 100% |
| Promotion | 8008 | ✅ 80% |
| AI | 8009 | ✅ 100% |
| Analytics | 8010 | ✅ 100% |
| **Frontend** | 3000 | ✅ 98% |

**Общий прогресс: 98%** 🎉

---

## 📁 Структура

```
teleflow/
├── docker-compose.yml      # Оркестрация
├── .env.example            # Конфиг
├── Makefile                # Команды
├── README.md               # Этот файл
├── DEVELOPMENT_STATUS.md   # Статус
├── FRONTEND_SPEC.md        # ТЗ на фронтенд
│
├── infra/                  # Инфраструктура
├── shared/                 # Shared library
├── services/               # 9 микросервисов
└── frontend/               # React SPA
```

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| [README.md](README.md) | Вы здесь |
| [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) | Статус разработки |
| [FRONTEND_SPEC.md](FRONTEND_SPEC.md) | ТЗ на фронтенд |
| [QUICKSTART.md](QUICKSTART.md) | Быстрый старт |

**Расширенная документация:** [`/teleflow-docs/`](../teleflow-docs/)

---

## 🧪 Тесты

```bash
# Backend E2E
python3 e2e_test.py           # Content pipeline
python3 e2e_funnel_test.py    # Funnels
python3 e2e_broadcast_test.py # Broadcasts
python3 e2e_promotion_test.py # Promotion
python3 e2e_ai_analytics_test.py # AI & Analytics

# Результат: 11/11 тестов ✅
```

---

## 🔗 Ссылки

| Сервис | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Grafana | http://localhost:3001 (admin/admin) |
| Prometheus | http://localhost:9090 |
| Traefik | http://localhost:8080 |
| RSSHub | http://localhost:1200 |

---

## 📞 Контакты

- **GitHub:** https://github.com/rabot1ga/teleflow-mvp
- **Ветка:** `frontend-tests`
- **Issues:** https://github.com/rabot1ga/teleflow-mvp/issues

---

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

*Последнее обновление: 12 марта 2026*
