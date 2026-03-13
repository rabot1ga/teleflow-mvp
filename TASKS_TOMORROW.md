# 📋 TeleFlow - Задачи на завтра

**Дата:** 13 марта 2026
**Спринт:** Q1 2026 - Week 12

---

## 🎯 Приоритеты

### 🔴 Высокий приоритет
1. Dashboard графики (Recharts)
2. Mobile адаптация
3. Исправление Content страницы

### 🟡 Средний приоритет
1. Dark theme
2. Backend сервисы (Userbot, AI)
3. Тесты

### 🟢 Низкий приоритет
1. Документация
2. CI/CD настройка

---

## 📱 Frontend Tasks

### 1. Dashboard Graphs ⏳ 4h
**Файлы:** `src/pages/dashboard/DashboardPage.tsx`

- [ ] Установить Recharts: `npm install recharts`
- [ ] Создать компонент `ActivityChart`
  - [ ] Area chart для активности по дням
  - [ ] Данные из API analytics
  - [ ] Tooltip с деталями
  - [ ] Legend с переключением
- [ ] Создать компонент `CategoryPieChart`
  - [ ] Pie chart для категорий
  - [ ] Legend с процентами
- [ ] Создать компонент `TrendLineChart`
  - [ ] Line chart для трендов
  - [ ] Сравнение периодов
- [ ] Интегрировать в Dashboard
  - [ ] Заменить placeholder на графики
  - [ ] Добавить loading states
  - [ ] Добавить empty states

**Ожидаемый результат:** Интерактивные графики на Dashboard

---

### 2. Mobile Adaptation ⏳ 3h
**Файлы:** Все страницы в `src/pages/`

- [ ] Проверить Dashboard на mobile (< 768px)
  - [ ] Stats grid → 1 колонка
  - [ ] Quick actions → 2 колонки
  - [ ] Sidebar → drawer menu
- [ ] Проверить Content страницу
  - [ ] Таблицы → horizontal scroll
  - [ ] Кнопки действий → compact
- [ ] Проверить Auth страницы
  - [ ] Форма → full width
  - [ ] Logo → smaller size
- [ ] Добавить mobile menu toggle
  - [ ] Hamburger button в header
  - [ ] Drawer animation
  - [ ] Backdrop (опционально)

**Ожидаемый результат:** Все страницы работают на mobile

---

### 3. Dark Theme ⏳ 3h
**Файлы:** `src/styles/tokens.css`

- [ ] Создать dark theme токены
  ```css
  [data-theme='dark'] {
    --tf-bg-app: #0f172a;
    --tf-bg-surface: #1e293b;
    --tf-text-primary: #f9fafb;
    /* ... остальные токены */
  }
  ```
- [ ] Добавить переключатель theme
  - [ ] Component `ThemeToggle`
  - [ ] Сохранение в localStorage
  - [ ] Apply к document.documentElement
- [ ] Протестировать все компоненты
  - [ ] Button (все variant)
  - [ ] Input (все states)
  - [ ] Card (gradient backgrounds)
  - [ ] Sidebar
- [ ] Проверить контрастность
  - [ ] Text на background
  - [ ] Icons на buttons

**Ожидаемый результат:** Working dark theme с переключателем

---

### 4. Content Page Improvements ⏳ 2h
**Файлы:** `src/pages/content/ContentPage.tsx`

- [ ] Улучшить UI таблиц
  - [ ] Добавить hover effects
  - [ ] Улучшить padding
  - [ ] Добавить compact mode
- [ ] Добавить фильтрацию
  - [ ] Filter by source type
  - [ ] Filter by status
  - [ ] Filter by date range
- [ ] Добавить поиск
  - [ ] Search input
  - [ ] Debounce 300ms
  - [ ] Highlight matches
- [ ] Улучшить pagination
  - [ ] Добавить page numbers
  - [ ] Добавить "Show X per page"
  - [ ] Добавить total count

**Ожидаемый результат:** Улучшенный UX для работы с контентом

---

## ⚙️ Backend Tasks

### 1. Userbot Service Activation ⏳ 2h
**Команда:** `docker compose up userbot-service`

- [ ] Изменить profile на `["dev", ""]`
- [ ] Применить миграции
- [ ] Проверить health check
- [ ] Протестировать API

**Ожидаемый результат:** Сервис доступен на порту 8007

---

### 2. AI Service Activation ⏳ 2h
**Команда:** `docker compose up ai-service`

- [ ] Изменить profile на `["dev", ""]`
- [ ] Применить миграции
- [ ] Проверить health check
- [ ] Протестировать API

**Ожидаемый результат:** Сервис доступен на порту 8009

---

### 3. WebSocket Integration ⏳ 3h
**Файлы:** `backend/services/*/app/websocket.py`

- [ ] Настроить WebSocket server
  - [ ] FastAPI WebSocket endpoint
  - [ ] Connection manager
  - [ ] Broadcast messages
- [ ] Добавить real-time события
  - [ ] article.approved
  - [ ] article.published
  - [ ] broadcast.started
  - [ ] broadcast.completed
- [ ] Интегрировать с frontend
  - [ ] Раскомментировать NotificationCenter
  - [ ] Подключение при загрузке
  - [ ] Обработка сообщений

**Ожидаемый результат:** Real-time уведомления в UI

---

## 🧪 Test Tasks

### 1. Publishing E2E Tests ⏳ 2h
**Файл:** `frontend/e2e/publishing/publishing.spec.ts`

- [ ] Тест создания Target
- [ ] Тест создания Template
- [ ] Тест переключения табов
- [ ] Тест удаления

**Ожидаемый результат:** 12/12 тестов проходят

---

### 2. Funnels E2E Tests ⏳ 2h
**Файл:** `frontend/e2e/funnels/funnels.spec.ts`

- [ ] Тест создания Funnel
- [ ] Тест создания Lead Magnet
- [ ] Тест создания Broadcast
- [ ] Тест запуска Broadcast

**Ожидаемый результат:** 8/8 тестов проходят

---

### 3. Visual Regression Tests ⏳ 3h
**Инструмент:** Playwright screenshots

- [ ] Настроить screenshot tests
- [ ] Сделать baseline скриншоты
  - [ ] Login page
  - [ ] Dashboard
  - [ ] Content page
- [ ] Добавить в CI/CD

**Ожидаемый результат:** Автоматическая проверка визуальных изменений

---

## 📚 Documentation Tasks

### 1. API Documentation ⏳ 2h
**Инструмент:** FastAPI Swagger

- [ ] Обновить OpenAPI spec
- [ ] Добавить примеры запросов
- [ ] Создать Postman collection
- [ ] Добавить описание endpoints

**Ожидаемый результат:** /docs показывает полную документацию

---

### 2. Screenshots ⏳ 1h
**Инструмент:** Скриншоты браузера

- [ ] Login page
- [ ] Dashboard
- [ ] Content page (все табы)
- [ ] Publishing page
- [ ] Funnels page
- [ ] Mobile views

**Ожидаемый результат:** Скриншоты в `/docs/screenshots/`

---

## 📊 План на день

### Утро (9:00 - 12:00)
- [ ] Dashboard Graphs (4h)

### Обед (12:00 - 13:00)

### День (13:00 - 17:00)
- [ ] Mobile Adaptation (3h)
- [ ] Dark Theme (3h)

### Вечер (17:00 - 18:00)
- [ ] Code review
- [ ] Commit изменений
- [ ] Update documentation

---

## 🎯 Definition of Done

Задача считается выполненной если:
- ✅ Код написан
- ✅ Тесты проходят
- ✅ Документация обновлена
- ✅ Code review пройден
- ✅ Задеплоено на staging

---

## 📈 Прогресс

```
Всего задач: 15
Выполнено: 0
В работе: 0
Осталось: 15

Прогресс: 0%
```

---

**Update в конце дня:**
- [ ] Обновить прогресс
- [ ] Добавить заметки
- [ ] Запланировать следующий день

---

*Created: 13 марта 2026*
