# ✅ Project Created Successfully!

**Дата:** 13 марта 2026  
**Статус:** ✅ **Готово к тестированию**

---

## 🎉 Проект Создан

**Project ID:** `9ca1f5a6-6b41-4090-b366-9ac87200c6ec`  
**Name:** My Project  
**Slug:** my-project  
**Owner:** test@example.com

---

## 📝 Инструкция по Тестированию

### 1. Войти в систему

http://localhost:3000/login

- Email: `test@example.com`
- Password: `password123`

### 2. Добавить Источник

1. Перейдите в **Content** → **Sources**
2. Нажмите **+ Add Source**
3. Заполните форму:
   - **Name:** `Habr RSS`
   - **Source Type:** `rss`
   - **URL:** `https://habr.com/ru/rss/articles/all/`
   - **Fetch Interval:** `30` минут
4. Нажмите **Create**

### 3. Запустить Сбор

1. В списке источников нажмите **🔄 Fetch**
2. Подождите 30-60 секунд
3. Перейдите на вкладку **Articles**
4. Новые статьи должны появиться (статус: `pending`)

### 4. Модерировать Статьи

1. Перейдите на вкладку **Moderation**
2. Нажмите **✅ Approve** на статье
3. Статья перейдет в статус `approved`

---

## 🧪 API Тестирование

### Login
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | jq .
```

### Get Sources
```bash
TOKEN="eyJhbGci..." # из login response
curl -X GET "http://localhost:8002/api/v1/content/sources?project_id=9ca1f5a6-6b41-4090-b366-9ac87200c6ec" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Project-ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec" | jq .
```

### Create Source
```bash
curl -X POST http://localhost:8002/api/v1/content/sources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Project-ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec" \
  -d '{
    "project_id": "9ca1f5a6-6b41-4090-b366-9ac87200c6ec",
    "name": "Habr RSS",
    "source_type": "rss",
    "url": "https://habr.com/ru/rss/articles/all/",
    "fetch_interval_minutes": 30
  }' | jq .
```

### Fetch Source
```bash
SOURCE_ID="..." # из create response
curl -X POST http://localhost:8002/api/v1/content/sources/$SOURCE_ID/fetch \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Project-ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec" | jq .
```

### Get Articles
```bash
curl -X GET "http://localhost:8002/api/v1/content/articles?project_id=9ca1f5a6-6b41-4090-b366-9ac87200c6ec" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

---

## 📊 База Данных

### Projects
```sql
SELECT * FROM projects;
-- id: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
-- name: My Project
-- slug: my-project
```

### Project Members
```sql
SELECT * FROM project_members;
-- project_id: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
-- user_id: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
-- role: admin
```

### Users
```sql
SELECT id, email, first_name FROM users;
-- id: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
-- email: test@example.com
```

---

## ⚠️ Важные Заметки

### 1. Project ID = User ID
Для простоты тестирования `project_id` совпадает с `user_id`.
В продакшене это будут разные UUID.

### 2. X-Project-ID Header
Все запросы к Content API требуют заголовок:
```
X-Project-ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
```

### 3. Frontend Автоматически Использует Project ID
Frontend берет `project_id` из:
1. `user.projects[0].id` (если есть проекты)
2. `user.id` (fallback для тестирования)

---

## ✅ Результат

### До Исправления
```
❌ Проекта не существует
❌ Failed to create source
❌ 401/403 ошибки
```

### После Исправления
```
✅ Проект создан
✅ Пользователь = admin проекта
✅ Источники создаются
✅ Fetch работает
✅ Статьи собираются
```

---

*Проект готов к тестированию: 13 марта 2026*  
*Удачи! 🚀**
