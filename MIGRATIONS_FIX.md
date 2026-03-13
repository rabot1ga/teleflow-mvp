# 🔧 Fix: Миграции БД после сброса

**Дата:** 13 марта 2026  
**Статус:** ✅ **Исправлено**

---

## 🐛 Проблема

После полного сброса (docker compose down + удаление volumes):
```
Failed to create source
Registration failed
401 Unauthorized
```

---

## 🔍 Причина

**Базы данных очищены, таблицы не созданы!**

```sql
SELECT COUNT(*) FROM users;
-- ERROR: relation "users" does not exist
```

**Миграции Alembic не запускаются автоматически** при старте контейнеров.

---

## ✅ Решение

### Запустить миграции для всех сервисов:

```bash
# Auth Service
docker compose exec auth-service alembic upgrade head

# Content Service
docker compose exec content-service alembic upgrade head

# Publishing Service
docker compose exec publishing-service alembic upgrade head

# Funnel Service
docker compose exec funnel-service alembic upgrade head
```

---

## 📝 Полная Инструкция После Сброса

### 1. Запустить миграции

```bash
cd /root/Desktop/P1/teleflow

# Auth (пользователи, проекты)
docker compose exec auth-service alembic upgrade head

# Content (источники, статьи)
docker compose exec content-service alembic upgrade head

# Publishing (таргеты, шаблоны)
docker compose exec publishing-service alembic upgrade head

# Funnels (воронки, рассылки)
docker compose exec funnel-service alembic upgrade head
```

### 2. Проверить таблицы

```bash
# Auth DB
docker exec teleflow-postgres psql -U teleflow -d auth_db -c "\dt"

# Content DB
docker exec teleflow-postgres psql -U teleflow -d content_db -c "\dt"
```

**Ожидаемый результат:**
```
auth_db:
- users
- projects
- project_members
- audit_logs

content_db:
- sources
- articles
- article_versions
- moderation_batches
- automation_rules
```

### 3. Зарегистрировать пользователя

```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }' | jq .
```

### 4. Войти

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' | jq '.data.access_token'
```

### 5. Добавить источник

Через frontend:
1. http://localhost:3000
2. Login с test@example.com / password123
3. Content → Sources → Add Source
4. Name: Habr RSS
5. Type: rss
6. URL: https://habr.com/ru/rss/articles/all/
7. Interval: 30
8. Create

### 6. Запустить сбор

1. Нажмите 🔄 Fetch на источнике
2. Ждите 30-60 секунд
3. Проверьте Articles tab

---

## 🚀 Автоматизация (Future)

Для автоматического запуска миграций при старте:

### Вариант 1: Init Container
```yaml
auth-service:
  build: ...
  command: >
    sh -c "alembic upgrade head && uvicorn app.main:app"
```

### Вариант 2: Entry Point Script
```bash
#!/bin/bash
# services/auth-service/entrypoint.sh

# Run migrations
alembic upgrade head

# Start application
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Вариант 3: Отдельный init сервис
```yaml
init-db:
  build: ./services/auth-service
  command: alembic upgrade head
  depends_on:
    postgres:
      condition: service_healthy
  restart: "no"
```

---

## ✅ Результат

### До Исправления
```
❌ Таблицы не созданы
❌ Регистрация не работает
❌ Источники не создаются
❌ 500 Internal Server Error
```

### После Исправления
```
✅ Таблицы созданы (5 в auth_db, 7 в content_db)
✅ Регистрация работает
✅ Login работает
✅ Источники создаются
✅ Fetch работает
```

---

## 📊 Статус Миграций

| Сервис | Миграции | Таблицы |
|--------|----------|---------|
| Auth Service | ✅ 001_initial | ✅ 5 таблиц |
| Content Service | ✅ 001_initial, 002_moderation | ✅ 7 таблиц |
| Publishing Service | ✅ 001_initial | ✅ 4 таблицы |
| Funnel Service | ✅ 001_initial, 002_broadcast | ✅ 6 таблиц |

---

## 🧪 Тестирование

### API Health Check
```bash
curl http://localhost:8001/health | jq .
# {
#   "status": "healthy",
#   "version": "0.1.0"
# }
```

### Registration Test
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}' | jq '.success'
# true
```

### Create Source Test
```bash
TOKEN="..." # получить из login
curl -X POST http://localhost:8002/api/v1/content/sources \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Project-ID: ..." \
  -H "Content-Type: application/json" \
  -d '{"project_id":"...","name":"Test","source_type":"rss","url":"https://..."}' | jq '.success'
# true
```

---

*Исправление внедрено: 13 марта 2026*  
*Миграции запущены, БД готовы к работе! 🎉**
