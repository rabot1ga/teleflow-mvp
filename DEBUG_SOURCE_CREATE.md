# 🔧 Debug: Failed to Create Source

**Дата:** 13 марта 2026  
**Статус:** 🔍 **Debug Mode Включен**

---

## ✅ Что Сделано

### 1. Обновлен Project ID по умолчанию
```typescript
let projectId = '9ca1f5a6-6b41-4090-b366-9ac87200c6ec' // Default test project ID
```

### 2. Добавлено Логирование
```typescript
console.log('📝 Creating source with data:', data)
console.log('🔑 Using project_id:', projectId)
console.log('✅ API response:', response.data)
console.error('❌ Create error:', error)
console.error('❌ Error response:', error.response?.data)
```

### 3. Улучшена Обработка Ошибок
Теперь показывает правильную ошибку из:
- `errorData.error.message`
- `errorData.detail`
- `errorData.message`
- `errorData` (string)

### 4. Добавлена Проверка
```typescript
enabled: !!projectId, // Only run if projectId is defined
```

---

## 📝 Инструкция по Отладке

### 1. Откройте Browser Console

**Chrome/Edge:**
- F12 → Console tab
- Или Ctrl+Shift+J

**Firefox:**
- F12 → Console tab
- Или Ctrl+Shift+K

### 2. Войдите в Систему

http://localhost:3000/login
- Email: `test@example.com`
- Password: `password123`

### 3. Попробуйте Добавить Источник

1. Content → Sources → + Add Source
2. Заполните форму
3. Нажмите Create

### 4. Проверьте Console Логи

**Ожидаемые логи:**
```
🔑 Project ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
📦 Auth storage: {id: "...", email: "..."}
📝 Creating source with data: {project_id: "...", name: "..."}
🔑 Using project_id: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec
```

**Если успех:**
```
✅ API response: {success: true, data: {...}}
✅ Source created: {success: true, data: {...}}
```

**Если ошибка:**
```
❌ Create error: {...}
❌ Error response: {...}
❌ Error status: 401/403/500
❌ Error headers: {...}
```

---

## 🐛 Возможные Проблемы и Решения

### 1. 401 Unauthorized

**Проблема:** Token не передается

**Решение:**
```javascript
// Проверить localStorage
localStorage.getItem('token')
// Должен вернуть JWT token
```

### 2. 403 Forbidden

**Проблема:** User не имеет прав на проект

**Решение:**
```javascript
// Проверить project membership
SELECT * FROM project_members WHERE user_id='...';
```

### 3. 400 Bad Request

**Проблема:** Неверные данные в запросе

**Решение:**
Проверить `console.log('📝 Creating source with data:')`

### 4. 500 Internal Server Error

**Проблема:** Ошибка на backend

**Решение:**
```bash
docker compose logs content-service --tail=50
```

---

## 🧪 Ручной Тест через API

### 1. Получить Token

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | jq '.data.access_token'
```

**Сохраните token:**
```bash
export TOKEN="eyJhbGci..."
```

### 2. Создать Источник

```bash
curl -X POST http://localhost:8002/api/v1/content/sources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Project-ID: 9ca1f5a6-6b41-4090-b366-9ac87200c6ec" \
  -d '{
    "project_id": "9ca1f5a6-6b41-4090-b366-9ac87200c6ec",
    "name": "Test RSS",
    "source_type": "rss",
    "url": "https://habr.com/ru/rss/articles/all/",
    "fetch_interval_minutes": 30
  }' | jq .
```

**Ожидаемый ответ:**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "name": "Test RSS",
    "source_type": "rss"
  }
}
```

---

## 📊 Проверка Базы Данных

### Источники
```bash
docker exec teleflow-postgres psql -U teleflow -d content_db -c "SELECT id, name, source_type, url FROM sources;"
```

### Пользователь и Проект
```bash
docker exec teleflow-postgres psql -U teleflow -d auth_db -c "SELECT id, email FROM users;"
docker exec teleflow-postgres psql -U teleflow -d auth_db -c "SELECT id, name, slug FROM projects;"
docker exec teleflow-postgres psql -U teleflow -d auth_db -c "SELECT * FROM project_members;"
```

---

## ✅ Следующие Шаги

1. **Откройте Browser Console (F12)**
2. **Попробуйте создать источник**
3. **Скопируйте логи из console**
4. **Отправьте логи для анализа**

---

*Debug mode включен: 13 марта 2026*  
*Ждем логи из browser console! 🔍**
