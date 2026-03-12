# 📐 TeleFlow Platform — Техническое Задание на Дизайн и Фронтенд

**Версия:** 1.0  
**Дата:** 12 марта 2026  
**Статус:** MVP готово (95%)  
**Ветка:** `frontend-tests`

---

## 📋 Содержание

1. [Обзор проекта](#обзор-проекта)
2. [Дизайн-система](#дизайн-система)
3. [Структура приложения](#структура-приложения)
4. [Описание страниц](#описание-страниц)
5. [UI Компоненты](#ui-компоненты)
6. [Технические требования](#технические-требования)
7. [API Интеграция](#api-интеграция)
8. [Тестирование](#тестирование)

---

## 📖 Обзор проекта

**TeleFlow Platform** — модульная платформа для полного цикла работы с Telegram-каналами.

### Основные возможности

| Модуль | Описание |
|--------|----------|
| **Content Hub** | Агрегация контента из RSS, API, парсинг |
| **Модерация** | Ручная и автоматическая модерация материалов |
| **Публикация** | Планирование и публикация в Telegram каналы |
| **Воронки** | Создание воронок для ботов, лид-магниты |
| **Рассылки** | Массовые рассылки по базе пользователей |
| **Юзерботы** | Управление Telegram аккаунтами, авторизация |
| **Продвижение** | Парсинг, инвайтинг, масслукинг, комментинг |
| **AI** | AI-обработка контента (rewrite, summarize) |
| **Аналитика** | Дашборды, статистика, отчёты |
| **RSSHub** | RSS генератор для Telegram и других платформ |

### Точки взаимодействия

- **Web SPA** — React-приложение для управления платформой
- **Telegram Bot** — бот для модерации и взаимодействия
- **REST API** — полный доступ ко всем функциям платформы

---

## 🎨 Дизайн-система

### Цветовая палитра

#### Primary (Modern Blue)
```css
--tf-primary-50:  #eff6ff
--tf-primary-100: #dbeafe
--tf-primary-200: #bfdbfe
--tf-primary-300: #93c5fd
--tf-primary-400: #60a5fa
--tf-primary-500: #3b82f6  ← Основной
--tf-primary-600: #2563eb
--tf-primary-700: #1d4ed8
--tf-primary-800: #1e40af
--tf-primary-900: #1e3a8a
```

#### Success (Emerald)
```css
--tf-success-50:  #ecfdf5
--tf-success-500: #10b981
--tf-success-600: #059669  ← Основной
--tf-success-700: #047857
```

#### Danger (Rose)
```css
--tf-danger-50:  #fff1f2
--tf-danger-500: #f43f5e
--tf-danger-600: #e11d48  ← Основной
--tf-danger-700: #be123c
```

#### Warning (Amber)
```css
--tf-warning-50:  #fffbeb
--tf-warning-500: #f59e0b
--tf-warning-600: #d97706  ← Основной
--tf-warning-700: #b45309
```

#### Neutral (Slate)
```css
--tf-slate-50:  #f8fafc
--tf-slate-100: #f1f5f9
--tf-slate-200: #e2e8f0
--tf-slate-300: #cbd5e1
--tf-slate-400: #94a3b8
--tf-slate-500: #64748b
--tf-slate-600: #475569
--tf-slate-700: #334155
--tf-slate-800: #1e293b
--tf-slate-900: #0f172a
```

### Типографика

#### Шрифты
```css
--tf-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
--tf-font-mono: 'JetBrains Mono', 'Fira Code', monospace
```

#### Размеры шрифтов
```
--tf-font-size-xs:   0.75rem   (12px)
--tf-font-size-sm:   0.875rem  (14px)
--tf-font-size-base: 1rem      (16px)
--tf-font-size-lg:   1.125rem  (18px)
--tf-font-size-xl:   1.25rem   (20px)
--tf-font-size-2xl:  1.5rem    (24px)
--tf-font-size-3xl:  1.875rem  (30px)
```

#### Насыщенность
```
--tf-font-weight-normal:   400
--tf-font-weight-medium:   500
--tf-font-weight-semibold: 600
--tf-font-weight-bold:     700
```

### Размеры и отступы

#### Spacing Scale
```
--tf-spacing-1:  0.25rem  (4px)
--tf-spacing-2:  0.5rem   (8px)
--tf-spacing-3:  0.75rem  (12px)
--tf-spacing-4:  1rem     (16px)
--tf-spacing-5:  1.25rem  (20px)
--tf-spacing-6:  1.5rem   (24px)
--tf-spacing-8:  2rem     (32px)
--tf-spacing-10: 2.5rem   (40px)
--tf-spacing-12: 3rem     (48px)
```

#### Border Radius
```
--tf-radius-sm:   0.25rem
--tf-radius-md:   0.375rem
--tf-radius-lg:   0.5rem
--tf-radius-xl:   0.75rem
--tf-radius-2xl:  1rem
--tf-radius-full: 9999px
```

### Тени
```css
--tf-shadow-xs: 0 1px 2px 0 var(--tf-shadow-color);
--tf-shadow-sm: 0 1px 3px 0 var(--tf-shadow-color), 0 1px 2px -1px var(--tf-shadow-color);
--tf-shadow-md: 0 4px 6px -1px var(--tf-shadow-color), 0 2px 4px -2px var(--tf-shadow-color);
--tf-shadow-lg: 0 10px 15px -3px var(--tf-shadow-color), 0 4px 6px -4px var(--tf-shadow-color);
--tf-shadow-xl: 0 20px 25px -5px var(--tf-shadow-color), 0 8px 10px -6px var(--tf-shadow-color);
```

### Анимации
```css
--tf-transition-fast:   150ms cubic-bezier(0.4, 0, 0.2, 1)
--tf-transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1)
--tf-transition-slow:   350ms cubic-bezier(0.4, 0, 0.2, 1)
```

---

## 🏗 Структура приложения

### Архитектура фронтенда

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AuthLayout.tsx      # Layout для страниц авторизации
│   │   │   └── DashboardLayout.tsx # Layout для dashboard с sidebar
│   │   └── ui/
│   │       ├── Button.tsx          # Кнопки (7 вариантов)
│   │       ├── Card.tsx            # Карточки
│   │       ├── StatCard.tsx        # Карточки статистики
│   │       ├── PageHeader.tsx      # Заголовки страниц
│   │       ├── Badge.tsx           # Бейджи
│   │       ├── Modal.tsx           # Модальные окна
│   │       ├── Table.tsx           # Таблицы
│   │       ├── Form.tsx            # Формы
│   │       ├── Input.tsx           # Поля ввода
│   │       ├── Select.tsx          # Выпадающие списки
│   │       ├── Search.tsx          # Поиск
│   │       ├── Skeleton.tsx        # Skeleton загрузкa
│   │       ├── Breadcrumbs.tsx     # Хлебные крошки
│   │       ├── EmptyState.tsx      # Пустые состояния
│   │       ├── Tabs.tsx            # Табы
│   │       └── Charts.tsx          # Графики (заглушки)
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx       # Страница входа
│   │   │   ├── RegisterPage.tsx    # Страница регистрации
│   │   │   ├── ForgotPasswordPage.tsx
│   │   │   └── ResetPasswordPage.tsx
│   │   ├── dashboard/
│   │   │   └── DashboardPage.tsx   # Главная страница
│   │   ├── content/
│   │   │   └── ContentPage.tsx     # Управление контентом (Sources, Articles, Moderation)
│   │   ├── publishing/
│   │   │   └── PublishingPage.tsx  # Публикация (Targets, Templates, Calendar)
│   │   ├── funnels/
│   │   │   └── FunnelsPage.tsx     # Воронки (Funnels, Lead Magnets, Broadcasts)
│   │   ├── userbot/
│   │   │   └── UserbotPage.tsx     # Юзерботы (Accounts, Proxies)
│   │   ├── promotion/
│   │   │   └── PromotionPage.tsx   # Продвижение (Tasks)
│   │   ├── analytics/
│   │   │   └── AnalyticsPage.tsx   # Аналитика (Overview, Content, Funnels)
│   │   └── settings/
│   │       └── SettingsPage.tsx    # Настройки (Profile, Project)
│   ├── services/
│   │   ├── api.ts                  # API client (axios)
│   │   ├── authApi.ts              # Auth API
│   │   ├── contentApi.ts           # Content API
│   │   ├── funnelApi.ts            # Funnels API
│   │   └── ...
│   ├── stores/
│   │   ├── authStore.ts            # Auth state (Zustand)
│   │   └── ...
│   ├── styles/
│   │   ├── design-tokens.css       # CSS переменные
│   │   └── main.css                # Базовые стили
│   ├── utils/
│   │   └── cn.ts                   # Class names helper
│   ├── App.tsx                     # Роутинг
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
└── ...
```

### Роутинг

```typescript
// Публичные маршруты
/login          → LoginPage
/register       → RegisterPage
/forgot-password → ForgotPasswordPage
/reset-password → ResetPasswordPage

// Защищённые маршруты (требуют авторизации)
/dashboard      → DashboardPage
/content        → ContentPage (Sources, Articles, Moderation tabs)
/publishing     → PublishingPage (Targets, Templates, Calendar tabs)
/funnels        → FunnelsPage (Funnels, Lead Magnets, Broadcasts tabs)
/userbot        → UserbotPage (Accounts, Proxies tabs)
/promotion      → PromotionPage (Tasks tab)
/analytics      → AnalyticsPage (Overview, Content, Funnels, Broadcasts tabs)
/settings       → SettingsPage (Profile, Project tabs)
```

---

## 📄 Описание страниц

### 1. Auth Layout

**Файл:** `src/components/layout/AuthLayout.tsx`

**Описание:** Layout для страниц авторизации с градиентным фоном.

**Элементы:**
- Градиентный фон с плавающими анимациями
- Логотип TeleFlow (⚡)
- Карточка формы по центру
- Footer с копирайтом

**Стили:**
- Background: linear-gradient(135deg, #1e3a8a → #0f172a)
- Floating circles animation
- Glassmorphism card effect

---

### 2. Login Page

**Файл:** `src/pages/auth/LoginPage.tsx`

**URL:** `/login`

**Элементы:**
- Заголовок: "🚀 TeleFlow"
- Подзаголовок: "Sign in to your account"
- Поле Email (input type="email")
- Поле Password (input type="password")
- Checkbox "Remember me"
- Ссылка "Forgot password?"
- Кнопка "Sign In"
- Кнопка "Sign in with Telegram" (✈️)
- Ссылка "Sign up"

**Валидация:**
- Email: required, valid email format
- Password: min 6 characters

**Состояния:**
- Loading (кнопка disabled)
- Error (alert с сообщением)
- Success (toast + redirect to /dashboard)

---

### 3. Register Page

**Файл:** `src/pages/auth/RegisterPage.tsx`

**URL:** `/register`

**Элементы:**
- Заголовок: "Create Account"
- First Name (input)
- Last Name (input)
- Email (input type="email")
- Password (input type="password")
- Confirm Password (input type="password")
- Кнопка "Create Account"
- Ссылка "Sign in"

**Валидация:**
- First Name: required
- Last Name: required
- Email: required, valid email
- Password: min 8 characters
- Confirm Password: must match password

**Состояния:**
- Loading
- Error (alert)
- Success (auto-login + redirect)

---

### 4. Dashboard Layout

**Файл:** `src/components/layout/DashboardLayout.tsx`

**Описание:** Основной layout с sidebar для всех защищённых страниц.

**Элементы:**

#### Sidebar (280px, collapsible to 80px)
- Логотип: ⚡ TeleFlow
- Кнопка collapse (◀ / ▶)
- Навигация по категориям:
  - **Main:** Dashboard (📊)
  - **Content:** Content (📰), Publishing (📤)
  - **Growth:** Funnels (🎯), Userbot (🤖), Promotion (📈)
  - **Analytics:** Analytics (📉)
  - **Settings:** Settings (⚙️)
- User info в footer:
  - Avatar (first letter)
  - Name
  - Email

#### Header
- Menu toggle (☰) для мобильных
- Заголовок страницы
- User menu dropdown:
  - Avatar
  - Name & Email
  - Settings link
  - Logout button

#### Main Content
- Outlet для страниц
- Padding: 24px

**Адаптивность:**
- Mobile: sidebar hidden, overlay backdrop
- Tablet: sidebar collapsible
- Desktop: sidebar expanded

---

### 5. Dashboard Page

**Файл:** `src/pages/dashboard/DashboardPage.tsx`

**URL:** `/dashboard`

**Элементы:**

#### Page Header
- Заголовок: "Dashboard"
- Описание: "Overview of your TeleFlow platform activity"

#### Stats Grid (4 карточки)
1. **Total Articles** (📰)
   - Value: 1,234
   - Trend: ↑ 12%
   
2. **Active Sources** (📡)
   - Value: 8
   - Trend: ↑ 2
   
3. **Active Funnels** (🎯)
   - Value: 5
   
4. **Subscribers** (👥)
   - Value: 2,847
   - Trend: ↑ 8%

#### Quick Actions Card
- Кнопки:
  - 📰 Add Source
  - 🎯 Create Funnel
  - 📤 New Broadcast
  - ⚙️ Settings

#### Recent Activity Card
- Empty state: 📭
- Текст: "No recent activity"

#### Content Overview (2 карточки)
- Content Performance (📈)
- Top Sources (🔥)

---

### 6. Content Page

**Файл:** `src/pages/content/ContentPage.tsx`

**URL:** `/content`

**Табы:**
- Sources
- Articles
- Moderation

#### Tab: Sources

**Элементы:**
- Кнопка "+ Add Source"
- Таблица источников:
  - Name
  - Type (RSS, JSON API, Scraper, Telegram, Webhook)
  - Interval (min)
  - Status (Active/Inactive badge)
  - Actions:
    - 🔄 Fetch (кнопка)
    - ✏️ Edit (кнопка)
    - 🗑️ Delete (кнопка)

**Modal: Add/Edit Source**

**Типы источников (quick select):**
- 📰 RSS Feed
- 🔗 RSSHub
- ✈️ Telegram
- 🔌 JSON API

**Поля формы:**
- Name (required)
- Source Type (select)
- URL (required для RSS/JSON API)
- RSSHub Path (для RSSHub)
  - Placeholder: "twitter/user/username"
  - Link: https://docs.rsshub.app
- Telegram Username (для Telegram)
  - Placeholder: "@durov"
- Fetch Interval (minutes, 5-1440)

**Динамические поля:**
- RSS: URL поле
- RSSHub: Path input с примерами
- Telegram: Username input
- JSON API: URL поле

#### Tab: Articles

**Элементы:**
- Заголовок: "Articles (count)"
- Таблица статей:
  - Title (+ summary)
  - Category
  - Status badge (pending/approved/rejected/published)
  - Priority score
  - Created date

**Empty state:**
- Текст: "No articles yet"
- Подсказка: "Go to Sources tab and click Fetch"

#### Tab: Moderation

**Элементы:**
- Заголовок: "Moderation Queue (count)"
- Таблица:
  - Title (+ priority, quality score)
  - Actions:
    - ✅ Approve (кнопка)
    - ❌ Reject (кнопка)

**Empty state:**
- Текст: "🎉 No articles pending moderation!"

---

### 7. Publishing Page

**Файл:** `src/pages/publishing/PublishingPage.tsx`

**URL:** `/publishing`

**Табы:**
- Targets
- Templates
- Calendar

#### Tab: Targets
- Список Telegram каналов
- Кнопка "Add Target"
- Target: name, username, status

#### Tab: Templates
- Шаблоны сообщений
- Кнопка "Create Template"
- Template editor с переменными

#### Tab: Calendar
- Календарь публикаций
- Drag & drop scheduling

---

### 8. Funnels Page

**Файл:** `src/pages/funnels/FunnelsPage.tsx`

**URL:** `/funnels`

**Табы:**
- Funnels
- Lead Magnets
- Broadcasts

#### Tab: Funnels
- Список воронок
- Кнопка "Create Funnel"
- Funnel: name, steps, status, entries

#### Tab: Lead Magnets
- Лид-магниты
- Кнопка "Create Lead Magnet"
- Type: text, file, link

#### Tab: Broadcasts
- Рассылки
- Кнопка "Create Broadcast"
- Broadcast: name, status, sent, delivered

---

### 9. Userbot Page

**Файл:** `src/pages/userbot/UserbotPage.tsx`

**URL:** `/userbot`

**Табы:**
- Accounts
- Proxies

#### Tab: Accounts
- Список Telegram аккаунтов
- Кнопка "Add Account"
- Account: name, phone, status, warming status
- Actions: authorize, edit, delete

#### Tab: Proxies
- Прокси для аккаунтов
- Кнопка "Add Proxy"
- Proxy: name, type, host, port

---

### 10. Promotion Page

**Файл:** `src/pages/promotion/PromotionPage.tsx`

**URL:** `/promotion`

**Таб:**
- Tasks

#### Tab: Tasks
- Список задач продвижения
- Кнопка "Create Task"
- Task types:
  - Parse users
  - Invite users
  - Masslook
  - Comment
- Task: name, type, status, progress, results

---

### 11. Analytics Page

**Файл:** `src/pages/analytics/AnalyticsPage.tsx`

**URL:** `/analytics`

**Табы:**
- Overview
- Content
- Funnels
- Broadcasts

#### Tab: Overview
- Stats cards
- Charts (заглушки)

#### Tab: Content
- Articles stats
- Sources performance

#### Tab: Funnels
- Funnel conversion
- Entries over time

#### Tab: Broadcasts
- Delivery stats
- Open rates

---

### 12. Settings Page

**Файл:** `src/pages/settings/SettingsPage.tsx`

**URL:** `/settings`

**Табы:**
- Profile
- Project

#### Tab: Profile
- Edit profile
- Change password
- Telegram link

#### Tab: Project
- Project settings
- Members management
- RBAC roles

---

## 🧩 UI Компоненты

### Button

**Файл:** `src/components/ui/Button.tsx`

**Props:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'outline' | 'ghost'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
}
```

**Примеры:**
```tsx
<Button variant="primary">Click me</Button>
<Button variant="success" size="lg">Success</Button>
<Button variant="outline" isLoading>Loading</Button>
```

---

### Card

**Файл:** `src/components/ui/Card.tsx`

**Props:**
```typescript
interface CardProps {
  title?: string
  subtitle?: string
  action?: React.ReactNode
  footer?: React.ReactNode
  noPadding?: boolean
}
```

**Пример:**
```tsx
<Card title="Card Title" subtitle="Optional subtitle">
  Content goes here
</Card>
```

---

### StatCard

**Файл:** `src/components/ui/StatCard.tsx`

**Props:**
```typescript
interface StatCardProps {
  title: string
  value: string | number
  icon?: string
  trend?: { value: number; isPositive: boolean }
}
```

**Пример:**
```tsx
<StatCard
  title="Total Articles"
  value="1,234"
  icon="📰"
  trend={{ value: 12, isPositive: true }}
/>
```

---

### Modal

**Файл:** `src/components/ui/Modal.tsx`

**Props:**
```typescript
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  footer?: React.ReactNode
  size?: 'md' | 'lg' | 'xl'
}
```

---

### Table

**Файл:** `src/components/ui/Table.tsx`

**Props:**
```typescript
interface TableProps {
  data: any[]
  columns: Array<{
    key: string
    title: string
    render?: (item: any) => React.ReactNode
  }>
}
```

---

## 🔧 Технические требования

### Стек технологий

```json
{
  "react": "^18.x",
  "react-dom": "^18.x",
  "react-router-dom": "^6.x",
  "typescript": "^5.x",
  "vite": "^5.x",
  "zustand": "^4.x",
  "@tanstack/react-query": "^5.x",
  "axios": "^1.x",
  "react-hook-form": "^7.x",
  "zod": "^3.x",
  "recharts": "^2.x"
}
```

### Структура проекта

```
teleflow/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── styles/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── ...
```

### Code Style

- **TypeScript:** strict mode
- **ESLint:** recommended + React hooks
- **Prettier:** default config
- **Naming:**
  - Components: PascalCase
  - Files: PascalCase для компонентов
  - Utils: camelCase
  - CSS: BEM-like с префиксом `tf-`

---

## 🌐 API Интеграция

### Base URL

**Development:**
- Frontend: `http://localhost:3000`
- API Proxy: Vite dev server proxy
- Auth API: `http://host.docker.internal:8001`
- Content API: `http://host.docker.internal:8002`
- ...

**Production:**
- API Gateway: `https://api.teleflow.com`
- Frontend: `https://teleflow.com`

### Auth Flow

1. Login → POST `/api/v1/auth/login`
2. Save tokens (access + refresh)
3. Add `Authorization: Bearer {token}` to requests
4. Handle 401 → refresh token
5. Refresh failed → logout

### API Services

```typescript
// src/services/authApi.ts
export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post('/api/v1/auth/login', { email, password }),
  
  register: (email: string, password: string, firstName: string, lastName: string) =>
    apiClient.post('/api/v1/auth/register', { email, password, first_name: firstName, last_name: lastName }),
  
  me: () =>
    apiClient.get('/api/v1/auth/me'),
}
```

---

## 🧪 Тестирование

### Unit Tests (Vitest)

```bash
npm run test
```

**Покрытие:**
- UI компоненты (Button, Card, Modal)
- Utils functions
- Stores (authStore)

### E2E Tests (Playwright)

```bash
npm run test:e2e
```

**Сценарии:**
- Login → Dashboard
- Create Source → Fetch → Articles
- Create Funnel → Trigger
- Create Broadcast → Send

---

## 📱 Адаптивность

### Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
  /* Sidebar hidden, overlay */
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  /* Sidebar collapsible */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Sidebar expanded */
}
```

### Mobile-first

Все компоненты проектируются сначала для мобильных, затем масштабируются для планшетов и десктопов.

---

## 🎯 Roadmap

### Phase 1 (MVP) — ✅ Завершено
- [x] Auth (Login, Register)
- [x] Dashboard Layout
- [x] Dashboard Page
- [x] Content Page (Sources, Articles, Moderation)
- [x] Funnels Page
- [x] Publishing Page
- [x] Userbot Page
- [x] Promotion Page
- [x] Analytics Page
- [x] Settings Page

### Phase 2 (Q2 2026)
- [ ] Funnels visual builder (drag & drop)
- [ ] AI integration UI (OpenAI, Anthropic)
- [ ] Analytics charts (Recharts)
- [ ] WebSocket real-time updates
- [ ] Dark theme

### Phase 3 (Q3 2026)
- [ ] Mobile app (React Native)
- [ ] PWA support
- [ ] Advanced analytics
- [ ] Custom dashboards

---

## 📞 Контакты

**GitHub:** https://github.com/rabot1ga/teleflow-mvp  
**Ветка:** `frontend-tests`  
**Документация:** `/frontend/DESIGN_SYSTEM.md`

---

*Последнее обновление: 12 марта 2026, 21:00*
