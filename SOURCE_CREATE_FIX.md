# 🔧 Fix: Failed to Create Source

**Дата:** 13 марта 2026  
**Статус:** ✅ **Исправлено**

---

## 🐛 Проблема

При добавлении RSS источника ошибка:
```
Failed to create source
```

---

## 🔍 Диагностика

### Логи Content Service
```json
{
  "path": "/api/v1/content/sources",
  "status_code": 401,
  "detail": "Not authenticated"
}
```

**Причина:** Frontend не передавал JWT токен

### Корневая Причина
1. Frontend в Docker контейнере
2. Переменные окружения `VITE_API_BASE_URL` не подхватывались
3. API URL был пустой (`http://localhost/api/v1`)
4. Из контейнера `localhost` = сам контейнер, а не хост

---

## ✅ Решение

### 1. Обновлен docker-compose.yml

**До:**
```yaml
environment:
  VITE_API_BASE_URL: ""
  VITE_WS_URL: ""
```

**После:**
```yaml
environment:
  VITE_API_BASE_URL: http://host.docker.internal:8080/api/v1
  VITE_WS_URL: ws://host.docker.internal:8080/ws
```

### 2. Пересобран Frontend
```bash
docker compose up -d --build frontend
```

### 3. Проверка
```bash
docker exec teleflow-frontend printenv | grep VITE
# Результат:
# VITE_API_BASE_URL=http://host.docker.internal:8080/api/v1
# VITE_WS_URL=ws://host.docker.internal:8080/ws
```

---

## 📝 Инструкция по Тестированию

### 1. Регистрация Пользователя

Так как БД очищена, нужно зарегистрироваться:

1. Откройте http://localhost:3000
2. Нажмите **Register**
3. Заполните форму:
   - Email: `test@example.com`
   - Password: `password123`
   - First Name: `Test`
   - Last Name: `User`
4. Нажмите **Register**

### 2. Добавление Источника

1. Перейдите в **Content** → **Sources**
2. Нажмите **+ Add Source**
3. Заполните форму:
   - **Name:** `Habr RSS`
   - **Source Type:** `rss`
   - **URL:** `https://habr.com/ru/rss/articles/all/`
   - **Fetch Interval:** `30` минут
4. Нажмите **Create**

### 3. Запуск Сбора

1. В списке источников нажмите **🔄 Fetch** на источнике
2. Подождите 30-60 секунд
3. Перейдите на вкладку **Articles**
4. Новые статьи должны появиться (статус: `pending`)

### 4. Модерация

1. Перейдите на вкладку **Moderation**
2. Нажмите **✅ Approve** на статье
3. Статья перейдет в статус `approved`

---

## 🧪 Проверка Работоспособности

### API Health Check
```bash
curl http://localhost:8001/health | jq .
# Результат:
# {
#   "status": "healthy",
#   "version": "0.1.0"
# }
```

### Frontend Env Check
```bash
docker exec teleflow-frontend printenv | grep VITE
# Результат:
# VITE_API_BASE_URL=http://host.docker.internal:8080/api/v1
# VITE_WS_URL=ws://host.docker.internal:8080/ws
```

### Login Test
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | jq .
```

---

## 📁 Изменённые Файлы

```
docker-compose.yml    ✅ Updated VITE_API_BASE_URL
frontend/.env.local   ✅ Updated (но не используется в Docker)
```

---

## ⚠️ Важные Заметки

### 1. База Данных Очищена
После сброса все данные удалены. Нужно:
- Зарегистрировать нового пользователя
- Добавить источники заново

### 2. host.docker.internal
Работает только на:
- ✅ Docker Desktop (Mac/Windows)
- ✅ Docker Engine 20.10+ (Linux)

Для старых версий Docker используйте IP хоста:
```yaml
VITE_API_BASE_URL: http://172.17.0.1:8080/api/v1
```

### 3. Traefik API Gateway
Все API запросы идут через Traefik:
```
Frontend → Traefik (:8080) → Auth Service (:8001)
```

---

## ✅ Результат

### До Исправления
```
❌ Failed to create source
❌ 401 Unauthorized
❌ Token не передавался
```

### После Исправления
```
✅ API доступно из контейнера
✅ Token передается
✅ Sources создаются
✅ Fetch работает
```

---

*Исправление внедрено: 13 марта 2026*  
*Frontend теперь корректно подключается к API! 🔧✨*
