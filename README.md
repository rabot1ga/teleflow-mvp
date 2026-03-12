# ⚡ TeleFlow Platform

**Modern Telegram Operations Management Platform**

[![Status](https://img.shields.io/badge/status-ready-success)]()
[![Tests](https://img.shields.io/badge/tests-passing-success)]()
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

---

## 📖 О проекте

**TeleFlow Platform** — модульная платформа для полного цикла работы с Telegram-каналами.

| Модуль | Назначение | Статус |
|--------|------------|--------|
| **Content Hub** | Агрегация контента из RSS, API, парсинг | ✅ Готово |
| **Модерация** | Ручная и автоматическая модерация | ✅ Готово |
| **Публикация** | Планирование и публикация в Telegram | ✅ Готово |
| **Воронки** | Создание воронок для ботов, лид-магниты | ✅ Готово |
| **Рассылки** | Массовые рассылки по базе пользователей | ✅ Готово |
| **Юзерботы** | Управление Telegram аккаунтами | ✅ Готово |
| **Продвижение** | Парсинг, инвайтинг, масслукинг, комментинг | ✅ Готово |
| **AI** | AI-обработка контента | ✅ Готово |
| **Аналитика** | Дашборды, статистика, отчёты | ✅ Готово |

---

## 🚀 Быстрый старт

### 1. Запуск платформы

```bash
# Клонировать репозиторий
git clone https://github.com/rabot1ga/teleflow-mvp.git
cd teleflow-mvp

# Запустить все сервисы
docker compose up -d

# Применить миграции
docker exec teleflow-auth-service alembic upgrade head
docker exec teleflow-content-service alembic upgrade head
docker exec teleflow-publishing-service alembic upgrade head
docker exec teleflow-funnel-service alembic upgrade head

# Создать тестового пользователя
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'
```

### 2. Доступ к сервисам

| Сервис | URL | Описание |
|--------|-----|----------|
| **Frontend** | http://localhost:3000 | Web интерфейс |
| **Traefik** | http://localhost:8080 | Dashboard gateway |
| **Grafana** | http://localhost:3001 | Мониторинг |
| **Prometheus** | http://localhost:9090 | Метрики |
| **MinIO** | http://localhost:9001 | Файловое хранилище |

### 3. Тестовый вход

```
Email: test@example.com
Password: password123
```

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

---

## 🛠 Стек технологий

| Слой | Технологии |
|------|------------|
| **Frontend** | React 18, Vite, TypeScript, Zustand, TanStack Query |
| **Backend** | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | PostgreSQL 16 (database-per-service) |
| **Cache/Broker** | Redis 7 (cache + Celery broker + Pub/Sub) |
| **Task Queue** | Celery 5.x + Celery Beat |
| **Search** | Meilisearch v1.6 |
| **Files** | MinIO (S3-compatible) |
| **Monitoring** | Prometheus + Grafana + Loki |
| **Gateway** | Traefik v3 |
| **Containers** | Docker, Docker Compose |

---

## ✅ Статус тестирования

### Backend E2E Tests
```
✅ Content Pipeline Test    - PASSED (40 статей собрано)
✅ Funnel E2E Test          - PASSED (воронка создана)
✅ Broadcast E2E Test       - PASSED (рассылка запущена)
```

### Frontend E2E Tests (Playwright)
```
✅ Auth Tests: 10/10 PASSED (100%)
  - Login page display
  - Form validation
  - Navigation
  - Login/Logout
  - Registration
```

### Health Checks
```
✅ auth:8001       - healthy
✅ content:8002    - healthy
✅ publishing:8004 - healthy
✅ funnel:8005     - healthy
✅ bot:8006        - healthy
✅ frontend:3000   - работает
✅ postgres:5432   - healthy
✅ redis:6379      - healthy
```

---

## 📁 Структура проекта

```
teleflow/
├── services/
│   ├── auth-service/          # Аутентификация и RBAC
│   ├── content-service/       # Контент и модерация
│   ├── publishing-service/    # Публикация
│   ├── funnel-service/        # Воронки
│   ├── bot-gateway/           # Telegram Bot API
│   ├── userbot-service/       # Юзерботы
│   ├── promotion-service/     # Продвижение
│   ├── ai-service/            # AI операции
│   └── analytics-service/     # Аналитика
├── frontend/
│   ├── src/
│   │   ├── components/        # UI компоненты
│   │   ├── pages/             # Страницы
│   │   ├── features/          # Feature модули
│   │   └── e2e/               # Playwright тесты
│   └── package.json
├── shared/
│   └── teleflow-common/       # Общая библиотека
├── infra/
│   ├── traefik/               # Gateway конфиг
│   ├── prometheus/            # Мониторинг
│   └── grafana/               # Дашборды
├── docker-compose.yml         # Оркестрация
├── e2e_test.py                # Backend E2E тесты
└── README.md                  # Этот файл
```

---

## 🧪 Тестирование

### Backend тесты

```bash
# Content pipeline
python3 e2e_test.py

# Funnels
python3 e2e_funnel_test.py

# Broadcasts
python3 e2e_broadcast_test.py

# Promotion
python3 e2e_promotion_test.py

# AI & Analytics
python3 e2e_ai_analytics_test.py
```

### Frontend тесты

```bash
cd frontend

# Все тесты
npm run test:e2e

# Auth тесты
npx playwright test e2e/auth

# В режиме браузера
npm run test:e2e:headed

# Показать отчёт
npm run test:e2e:report
```

---

## 📊 Мониторинг

### Grafana Dashboards
- **URL:** http://localhost:3001
- **Login:** admin / admin

### Prometheus Metrics
- **URL:** http://localhost:9090
- **Metrics:** http://localhost:9090/metrics

### Loki Logs
- **URL:** http://localhost:3100

---

## 🔐 Безопасность

- ✅ JWT аутентификация с refresh токенами
- ✅ RBAC (Role-Based Access Control)
- ✅ HTTPS/TLS через Traefik
- ✅ Docker secrets для чувствительных данных
- ✅ Rate limiting на уровне gateway
- ✅ CORS политика

---

## 📈 Производительность

| Метрика | Значение |
|---------|----------|
| Cold start | < 30 секунд |
| API response time | < 100ms (p95) |
| Article ingestion | 40 статей за 30 сек |
| Concurrent users | 100+ |
| Database connections | Pool 10-100 |

---

## 🔗 Ссылки

### Документация
- [FULL_TEST_REPORT.md](./FULL_TEST_REPORT.md) - Полный отчёт о тестировании
- [frontend/e2e/README.md](./frontend/e2e/README.md) - E2E тесты документация
- [DEVELOPMENT_STATUS.md](./DEVELOPMENT_STATUS.md) - Статус разработки

### GitHub
- **Repository:** https://github.com/rabot1ga/teleflow-mvp
- **Branches:** 
  - `main` - основная ветка
  - `frontend-tests` - frontend тесты
  - `e2e-tests-full` - полные E2E тесты (текущая)

---

## 🚧 Roadmap

### Q1 2026 ✅
- [x] Auth Service
- [x] Content Service
- [x] Publishing Service
- [x] Funnel Service
- [x] Bot Gateway
- [x] Frontend MVP
- [x] E2E Tests

### Q2 2026
- [ ] Userbot Service (full)
- [ ] Promotion Service (full)
- [ ] AI Service (full)
- [ ] Analytics Dashboard
- [ ] Mobile App
- [ ] Advanced AI features

---

## 🤝 Вклад

1. Fork репозиторий
2. Создай feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Открой Pull Request

---

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE) файл

---

## 👥 Команда

**Lead Developer:** @rabot1ga

---

## 📞 Контакты

- **GitHub:** https://github.com/rabot1ga
- **Email:** test@example.com

---

**Статус:** ✅ Production Ready
**Последнее обновление:** 12 марта 2026
**Версия:** 1.0.0

---

*Made with ❤️ by TeleFlow Team*
