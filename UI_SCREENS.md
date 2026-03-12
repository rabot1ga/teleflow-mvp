# TeleFlow Platform — UI/UX Screens Specification

## 📱 Общее описание

**Frontend:** React 18 + Vite + TypeScript + Zustand + TanStack Query  
**UI Kit:** Bootstrap 5 + Material Design принципы  
**Роутинг:** React Router v6  
**Формы:** React Hook Form + Zod валидация

---

## 🎨 Структура приложения

```
src/
├── components/          # Переиспользуемые компоненты
│   ├── ui/             # Базовые UI компоненты
│   ├── layout/         # Layout компоненты
│   └── common/         # Общие компоненты
├── pages/              # Страницы приложения
│   ├── auth/           # Страницы аутентификации
│   ├── dashboard/      # Дашборд
│   ├── content/        # Контент модуль
│   ├── publishing/     # Публикация
│   ├── funnels/        # Воронки
│   ├── userbot/        # Юзерботы
│   ├── promotion/      # Продвижение
│   ├── analytics/      # Аналитика
│   └── settings/       # Настройки
├── stores/             # Zustand stores
├── hooks/              # Custom hooks
├── services/           # API clients
└── types/              # TypeScript types
```

---

## 📋 Экраны приложения

### 1. Аутентификация

#### 1.1 Login Page (`/login`)
**Функции:**
- Форма входа (email + password)
- Кнопка "Войти через Telegram"
- Ссылка "Забыли пароль?"
- Ссылка "Регистрация"

**Компоненты:**
- LoginForm
- TelegramLoginButton
- ForgotPasswordLink
- RegisterLink

**API:**
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/telegram/login-url`

---

#### 1.2 Register Page (`/register`)
**Функции:**
- Форма регистрации (email, password, confirm password, first_name, last_name)
- Валидация пароля (min 8 chars, 1 uppercase, 1 number)
- Чекбокс согласия с условиями
- Кнопка "Зарегистрироваться"

**Компоненты:**
- RegisterForm
- PasswordStrengthIndicator
- TermsCheckbox

**API:**
- `POST /api/v1/auth/register`

---

#### 1.3 Forgot Password Page (`/forgot-password`)
**Функции:**
- Ввод email для сброса пароля
- Отправка ссылки на сброс
- Сообщение об успешной отправке

**Компоненты:**
- ForgotPasswordForm
- SuccessMessage

**API:**
- `POST /api/v1/auth/forgot-password`

---

#### 1.4 Reset Password Page (`/reset-password/:token`)
**Функции:**
- Ввод нового пароля
- Подтверждение нового пароля
- Валидация пароля
- Кнопка "Сбросить пароль"

**Компоненты:**
- ResetPasswordForm
- PasswordStrengthIndicator

**API:**
- `POST /api/v1/auth/reset-password`

---

### 2. Dashboard (`/dashboard`)

**Функции:**
- Overview статистика за период (7/30/90 дней)
- Графики:
  - Статьи создано/опубликовано
  - Воронки: входы/завершения
  - Рассылки: отправлено/доставлено
  - Продвижение: спаршено/инвайчено
- Быстрые действия:
  - Создать статью
  - Запустить рассылку
  - Добавить источник
- Последние события
- Уведомления

**Компоненты:**
- StatsCards (4 карточки)
- ArticlesChart (line chart)
- FunnelsChart (bar chart)
- RecentActivityList
- QuickActionsPanel
- NotificationsPanel

**API:**
- `GET /api/v1/analytics/dashboard/overview`
- `GET /api/v1/analytics/dashboard/content`
- `GET /api/v1/analytics/dashboard/funnels`
- `GET /api/v1/content/moderation/stats`

---

### 3. Content Module

#### 3.1 Sources List (`/content/sources`)
**Функции:**
- Список источников с фильтрами (тип, статус, проект)
- Поиск по названию
- Сортировка (по имени, дате создания, активности)
- Пагинация
- Кнопка "Добавить источник"
- Actions для каждого источника:
  - Редактировать
  - Удалить
  - Запустить сбор сейчас
  - Включить/Выключить

**Компоненты:**
- SourcesTable
- SourceFilters
- SourceStatusBadge
- Pagination
- AddSourceButton
- SourceActionsDropdown

**API:**
- `GET /api/v1/content/sources`
- `DELETE /api/v1/content/sources/{id}`
- `POST /api/v1/content/sources/{id}/fetch`

---

#### 3.2 Add/Edit Source (`/content/sources/new`, `/content/sources/:id/edit`)
**Функции:**
- Форма создания/редактирования источника:
  - Название
  - Тип источника (RSS, JSON API, Scraper, Telegram, Webhook)
  - URL
  - Интервал сбора (минуты)
  - Категория по умолчанию
  - Теги по умолчанию
  - Приоритет (-10 до +10)
  - Репутация (0-1)
- Валидация полей
- Кнопки "Сохранить" и "Отмена"
- Тест подключения (для API/Webhook)

**Компоненты:**
- SourceForm
- SourceTypeSelector
- FetchIntervalInput
- PrioritySlider
- ReputationInput
- TestConnectionButton

**API:**
- `POST /api/v1/content/sources`
- `PATCH /api/v1/content/sources/{id}`
- `POST /api/v1/content/sources/test-connection`

---

#### 3.3 Moderation Queue (`/content/moderation`)
**Функции:**
- Очередь статей на модерацию
- Фильтры:
  - Статус (pending, approved, rejected)
  - Категория
  - Источник
  - Дата
- Сортировка (по приоритету, дате)
- Пагинация
- Просмотр статьи (модальное окно):
  - Заголовок
  - Контент (с форматированием)
  - Изображение
  - Источник
  - Категория
  - Теги
  - Quality Score
  - Priority Score
- Действия:
  - Одобрить (с выбором канала для публикации)
  - Отклонить (с выбором причины и комментарием)
  - Редактировать
  - Запланировать публикацию
- Пакетная модерация (выбрать несколько → одобрить/отклонить)

**Компоненты:**
- ModerationQueue
- ArticleCard
- ArticlePreviewModal
- ArticleActions
- BatchModerationPanel
- FiltersPanel
- QualityScoreBadge
- PriorityBadge

**API:**
- `GET /api/v1/content/moderation/queue`
- `POST /api/v1/content/articles/{id}/approve`
- `POST /api/v1/content/articles/{id}/reject`
- `PATCH /api/v1/content/articles/{id}`
- `POST /api/v1/content/articles/{id}/schedule`
- `POST /api/v1/content/moderation/batches`

---

#### 3.4 Articles List (`/content/articles`)
**Функции:**
- Список всех статей
- Фильтры:
  - Статус
  - Категория
  - Источник
  - Дата создания
  - Опубликовано/нет
- Поиск по названию/контенту
- Сортировка
- Пагинация
- Экспорт (CSV, JSON)
- Actions:
  - Просмотр
  - Редактировать
  - Удалить
  - AI Rewrite
  - AI Summarize
  - AI Classify

**Компоненты:**
- ArticlesTable
- ArticleFilters
- ArticleStatusBadge
- ExportButton
- AIActionsDropdown

**API:**
- `GET /api/v1/content/articles`
- `DELETE /api/v1/content/articles/{id}`
- `POST /api/v1/content/ai/rewrite`
- `POST /api/v1/content/ai/summarize`
- `POST /api/v1/content/ai/classify`

---

#### 3.5 Article Editor (`/content/articles/:id/edit`)
**Функции:**
- Редактор статьи:
  - Заголовок
  - Контент (Rich Text Editor)
  - Изображение (загрузка/URL)
  - Категория (выбор)
  - Теги (autocomplete)
  - SEO поля (meta title, description)
- История версий (сравнение версий)
- AI операции:
  - Rewrite (выбор стиля и тона)
  - Summarize
  - Generate Tags
  - Classify
- Предпросмотр
- Сохранение черновика
- Публикация

**Компоненты:**
- RichTextEditor
- ImageUploader
- CategorySelector
- TagsInput
- VersionHistory
- AIActionsPanel
- PreviewPanel
- SaveDraftButton
- PublishButton

**API:**
- `GET /api/v1/content/articles/{id}`
- `PATCH /api/v1/content/articles/{id}`
- `GET /api/v1/content/articles/{id}/versions`
- `POST /api/v1/content/ai/rewrite`
- `POST /api/v1/content/ai/summarize`

---

#### 3.6 Automation Rules (`/content/rules`)
**Функции:**
- Список правил автоматизации
- Создание/редактирование правил:
  - Название
  - Описание
  - Приоритет
  - Условия (конструктор условий):
    - Поле (quality_score, category, source, etc.)
    - Оператор (eq, gt, lt, contains, etc.)
    - Значение
    - Логика (AND/OR)
  - Действия:
    - Auto approve
    - Auto reject
    - Set priority
    - Set category
    - Add tags
    - Send to AI
- Включить/Выключить правило
- Статистика срабатываний

**Компоненты:**
- RulesList
- RuleBuilder
- ConditionBuilder
- ActionBuilder
- RuleStatusToggle
- RuleStats

**API:**
- `GET /api/v1/content/rules`
- `POST /api/v1/content/rules`
- `PATCH /api/v1/content/rules/{id}`
- `DELETE /api/v1/content/rules/{id}`

---

### 4. Publishing Module

#### 4.1 Targets List (`/publishing/targets`)
**Функции:**
- Список целей публикации (Telegram каналы/чаты)
- Кнопка "Добавить цель"
- Форма добавления:
  - Название
  - Тип (channel, group)
  - Telegram Chat ID
  - Username (@channel)
  - Описание
- Статус подключения
- Actions:
  - Редактировать
  - Удалить
  - Тест публикации

**Компоненты:**
- TargetsTable
- TargetForm
- TargetStatusBadge
- TestPublishButton

**API:**
- `GET /api/v1/publishing/targets`
- `POST /api/v1/publishing/targets`
- `PATCH /api/v1/publishing/targets/{id}`
- `DELETE /api/v1/publishing/targets/{id}`

---

#### 4.2 Templates List (`/publishing/templates`)
**Функции:**
- Список шаблонов сообщений
- Кнопка "Создать шаблон"
- Редактор шаблонов:
  - Название
  - Контент шаблона с переменными:
    - `{{ title }}`
    - `{{ content }}`
    - `{{ source }}`
    - `{{ tags }}`
    - `{{ url }}`
  - Предпросмотр с примером данных
  - Шаблон по умолчанию (toggle)
- Actions:
  - Редактировать
  - Удалить
  - Дублировать

**Компоненты:**
- TemplatesList
- TemplateEditor
- TemplateVariablesHelp
- TemplatePreview
- SetAsDefaultButton

**API:**
- `GET /api/v1/publishing/templates`
- `POST /api/v1/publishing/templates`
- `PATCH /api/v1/publishing/templates/{id}`
- `DELETE /api/v1/publishing/templates/{id}`

---

#### 4.3 Publish Calendar (`/publishing/calendar`)
**Функции:**
- Календарь публикаций (месяц/неделя/день)
- Отображение запланированных публикаций
- Drag & Drop для изменения времени
- Клик на событие → детали публикации
- Кнопка "Запланировать публикацию"
- Фильтры по каналам

**Компоненты:**
- PublishCalendar
- PublishEvent
- PublishEventDetails
- SchedulePublishButton
- CalendarFilters

**API:**
- `GET /api/v1/publishing/jobs?status=scheduled`
- `PATCH /api/v1/publishing/jobs/{id}`

---

#### 4.4 Scheduled Jobs (`/publishing/jobs`)
**Функции:**
- Список запланированных публикаций
- Фильтры:
  - Статус (scheduled, published, failed)
  - Канал
  - Дата
- Сортировка
- Actions:
  - Просмотр деталей
  - Редактировать время
  - Отменить
  - Опубликовать сейчас

**Компоненты:**
- JobsTable
- JobStatusBadge
- JobDetailsModal
- PublishNowButton
- CancelJobButton

**API:**
- `GET /api/v1/publishing/jobs`
- `PATCH /api/v1/publishing/jobs/{id}`
- `DELETE /api/v1/publishing/jobs/{id}`

---

### 5. Funnels Module

#### 5.1 Funnels List (`/funnels`)
**Функции:**
- Список воронок
- Кнопка "Создать воронку"
- Статистика по каждой воронке:
  - Входов
  - Завершений
  - Конверсия
- Статус (активна/неактивна)
- Actions:
  - Редактировать
  - Дублировать
  - Включить/Выключить
  - Удалить

**Компоненты:**
- FunnelsTable
- FunnelStatsCard
- FunnelStatusToggle
- FunnelActionsDropdown

**API:**
- `GET /api/v1/funnels/funnels`
- `POST /api/v1/funnels/funnels`
- `PATCH /api/v1/funnels/funnels/{id}`
- `DELETE /api/v1/funnels/funnels/{id}`

---

#### 5.2 Funnel Builder (`/funnels/:id/build`)
**Функции:**
- Визуальный конструктор воронок
- Drag & Drop шаги
- Типы шагов:
  - Сообщение (text, photo, video)
  - Кнопки (inline, reply)
  - Задержка
  - Условие (if/else)
  - Действие (tag, subscribe)
- Настройка каждого шага:
  - Контент
  - Условия перехода
  - Задержки
- Тестирование воронки (preview)
- Сохранение

**Компоненты:**
- FunnelBuilder
- StepNode
- StepConfigPanel
- ConnectionLine
- FunnelPreview
- SaveFunnelButton

**API:**
- `GET /api/v1/funnels/funnels/{id}`
- `PATCH /api/v1/funnels/funnels/{id}`
- `POST /api/v1/funnels/funnels/{id}/steps`

---

#### 5.3 Lead Magnets (`/funnels/lead-magnets`)
**Функции:**
- Список лид-магнитов
- Кнопка "Создать лид-магнит"
- Типы:
  - Текст
  - Файл (PDF, DOC, etc.)
  - Ссылка
  - Промокод
- Форма создания:
  - Название
  - Тип
  - Контент
  - Сообщение доставки
  - Требовать подписку (toggle)
- Статистика выдач

**Компоненты:**
- LeadMagnetsList
- LeadMagnetForm
- LeadMagnetTypeSelector
- LeadMagnetStats

**API:**
- `GET /api/v1/funnels/lead-magnets`
- `POST /api/v1/funnels/lead-magnets`
- `PATCH /api/v1/funnels/lead-magnets/{id}`

---

#### 5.4 Broadcasts (`/funnels/broadcasts`)
**Функции:**
- Список рассылок
- Кнопка "Создать рассылку"
- Фильтры:
  - Статус (draft, running, completed, cancelled)
  - Дата
- Статистика:
  - Отправлено
  - Доставлено
  - Ошибки
- Actions:
  - Просмотр деталей
  - Запустить
  - Отменить
  - Дублировать

**Компоненты:**
- BroadcastsList
- BroadcastForm
- BroadcastStatusBadge
- BroadcastStats
- RecipientSelector
- LaunchBroadcastButton

**API:**
- `GET /api/v1/funnels/broadcasts`
- `POST /api/v1/funnels/broadcasts`
- `POST /api/v1/funnels/broadcasts/{id}/start`
- `POST /api/v1/funnels/broadcasts/{id}/cancel`

---

### 6. Userbot Module

#### 6.1 Accounts List (`/userbot/accounts`)
**Функции:**
- Список аккаунтов Telegram
- Кнопка "Добавить аккаунт"
- Статус каждого аккаунта:
  - Неактивный
  - Активный
  - Забанен
  - Нужна авторизация
  - Нужен 2FA
- Информация:
  - Имя
  - Username
  - Телефон (маскированный)
  - Прогрев (включен/выключен, день)
- Actions:
  - Авторизовать
  - Редактировать
  - Удалить
  - Включить прогрев

**Компоненты:**
- AccountsTable
- AccountStatusBadge
- WarmingStatusIndicator
- AuthorizeButton
- AccountActionsDropdown

**API:**
- `GET /api/v1/userbot/accounts`
- `POST /api/v1/userbot/accounts`
- `DELETE /api/v1/userbot/accounts/{id}`

---

#### 6.2 Add Account Wizard (`/userbot/accounts/new`)
**Функции:**
- Пошаговый мастер добавления:
  1. Ввод телефона
  2. Отправка кода
  3. Ввод кода из Telegram
  4. Ввод 2FA пароля (если требуется)
  5. Проверка подключения
  6. Готово
- Индикатор прогресса
- Таймер обратного отсчёта для повторной отправки кода

**Компоненты:**
- AddAccountWizard
- PhoneInputStep
- CodeInputStep
- TwoFAStep
- VerificationStep
- SuccessStep
- ResendCodeTimer

**API:**
- `POST /api/v1/userbot/accounts/{id}/send-code`
- `POST /api/v1/userbot/accounts/{id}/verify`
- `POST /api/v1/userbot/accounts/{id}/2fa`

---

#### 6.3 Proxies List (`/userbot/proxies`)
**Функции:**
- Список прокси
- Кнопка "Добавить прокси"
- Типы прокси:
  - MTProto
  - SOCKS5
  - HTTP
- Форма добавления:
  - Название
  - Тип
  - Hostname
  - Порт
  - Username/Password (опционально)
  - Secret (для MTProto)
- Тест подключения
- Статус (работает/не работает)
- Actions:
  - Редактировать
  - Удалить
  - Проверить

**Компоненты:**
- ProxiesTable
- ProxyForm
- ProxyTypeSelector
- TestProxyButton
- ProxyStatusBadge

**API:**
- `GET /api/v1/userbot/proxies`
- `POST /api/v1/userbot/proxies`
- `POST /api/v1/userbot/proxies/{id}/check`

---

#### 6.4 Warming Schedule (`/userbot/warming`)
**Функции:**
- Расписание прогрева для аккаунтов
- Настройка прогрева:
  - Длительность (7-30 дней)
  - Действия на день:
    - Вступить в каналы (кол-во)
    - Прочитать сообщения (кол-во)
    - Отправить сообщений (кол-во)
    - Реакции (кол-во)
  - Задержки между действиями
  - Рабочие часы
- Статус прогрева:
  - Текущий день
  - Прогресс
  - Следующее действие
- Лог действий

**Компоненты:**
- WarmingSchedule
- WarmingConfigForm
- WarmingProgressIndicator
- WarmingLog
- StartWarmingButton
- StopWarmingButton

**API:**
- `GET /api/v1/userbot/accounts/{id}/warming`
- `POST /api/v1/userbot/accounts/{id}/warming/start`
- `POST /api/v1/userbot/accounts/{id}/warming/stop`

---

### 7. Promotion Module

#### 7.1 Tasks List (`/promotion/tasks`)
**Функции:**
- Список задач продвижения
- Кнопка "Создать задачу"
- Типы задач:
  - Парсинг
  - Инвайтинг
  - Масслукинг
  - Комментинг
- Фильтры:
  - Тип
  - Статус (pending, running, completed, failed)
  - Дата
- Статистика задачи:
  - Всего
  - Успешно
  - Ошибки
- Actions:
  - Запустить
  - Отменить
  - Просмотреть результаты
  - Удалить

**Компоненты:**
- TasksTable
- TaskTypeBadge
- TaskStatusBadge
- TaskStats
- TaskActionsDropdown
- CreateTaskButton

**API:**
- `GET /api/v1/promotion/tasks`
- `POST /api/v1/promotion/tasks`
- `POST /api/v1/promotion/tasks/{id}/start`
- `POST /api/v1/promotion/tasks/{id}/cancel`

---

#### 7.2 Create Parse Task (`/promotion/tasks/parse/new`)
**Функции:**
- Мастер создания задачи парсинга:
  1. Название задачи
  2. Источник (чат для парсинга):
     - Ввод username/chat ID
     - Выбор из сохранённых
  3. Фильтры:
     - Активность (дней)
     - Наличие фото
     - Premium пользователи
     - Боты (включить/исключить)
  4. Лимиты:
     - Максимум пользователей
     - Userbot аккаунты для парсинга
  5. Подтверждение

**Компоненты:**
- ParseTaskWizard
- SourceSelector
- FiltersPanel
- LimitsPanel
- AccountSelector
- ConfirmStep

**API:**
- `POST /api/v1/promotion/tasks`
- `GET /api/v1/userbot/accounts`

---

#### 7.3 Create Invite Task (`/promotion/tasks/invite/new`)
**Функции:**
- Мастер создания задачи инвайтинга:
  1. Название задачи
  2. Цель (чат для инвайта)
  3. Источник пользователей:
     - Выбрать задачу парсинга
     - Загрузить список (CSV)
     - Вручную
  4. Настройки:
     - Максимум инвайтов на аккаунт
     - Задержка между инвайтами
     - Userbot аккаунты
  5. Фильтры:
     - Не приглашать уже приглашённых
     - Исключить по ID
  6. Подтверждение

**Компоненты:**
- InviteTaskWizard
- TargetSelector
- SourceSelector
- InviteSettings
- FiltersPanel
- AccountSelector

**API:**
- `POST /api/v1/promotion/tasks`
- `GET /api/v1/promotion/tasks/:id/parsed-users`

---

#### 7.4 Parsed Users (`/promotion/parsed-users`)
**Функции:**
- Список спарсенных пользователей
- Фильтры:
  - Задача парсинга
  - Статус (invited, not invited)
  - Наличие фото
  - Premium
- Поиск по username/ID
- Экспорт (CSV, JSON)
- Actions:
  - Просмотреть детали
  - Пригласить вручную
  - Добавить в чёрный список

**Компоненты:**
- ParsedUsersTable
- ParsedUserFilters
- ParsedUserDetailsModal
- InviteManuallyButton
- ExportButton

**API:**
- `GET /api/v1/promotion/parsed-users`
- `POST /api/v1/promotion/parsed-users/{id}/invite`

---

#### 7.5 Masslook Task (`/promotion/tasks/masslook/new`)
**Функции:**
- Мастер создания задачи масслукинга:
  1. Название задачи
  2. Целевые пользователи (usernames)
  3. Настройки:
     - Кол-во stories для просмотра
     - Задержка между просмотрами
     - Userbot аккаунты
  4. Расписание:
     - Одноразово
     - По расписанию (cron)
  5. Подтверждение

**Компоненты:**
- MasslookTaskWizard
- TargetUsersInput
- MasslookSettings
- ScheduleConfig
- AccountSelector

**API:**
- `POST /api/v1/promotion/tasks`

---

#### 7.6 Comment Task (`/promotion/tasks/comment/new`)
**Функции:**
- Мастер создания задачи комментинга:
  1. Название задачи
  2. Целевой чат/канал
  3. Текст комментария:
     - Редактор текста
     - Переменные ({{username}}, {{date}})
     - Список вариантов (спинтаксис)
  4. Настройки:
     - Кол-во комментариев на аккаунт
     - Задержка между комментариями
     - Userbot аккаунты
  5. Расписание
  6. Подтверждение

**Компоненты:**
- CommentTaskWizard
- CommentEditor
- SpintaxEditor
- CommentSettings
- ScheduleConfig

**API:**
- `POST /api/v1/promotion/tasks`

---

### 8. Analytics Module

#### 8.1 Overview Dashboard (`/analytics/overview`)
**Функции:**
- Выбор периода (7/30/90 дней, custom)
- Overview метрики:
  - Статьи (создано, одобрено, опубликовано)
  - Воронки (входы, завершения, конверсия)
  - Рассылки (отправлено, доставлено)
  - Продвижение (спаршено, инвайчено)
- Графики:
  - Динамика по дням
  - Сравнение периодов
- Топ источников
- Топ воронок

**Компоненты:**
- PeriodSelector
- MetricsCards
- TrendsChart
- TopSourcesList
- TopFunnelsList

**API:**
- `GET /api/v1/analytics/dashboard/overview`
- `GET /api/v1/analytics/dashboard/content`
- `GET /api/v1/analytics/dashboard/funnels`

---

#### 8.2 Content Analytics (`/analytics/content`)
**Функции:**
- Статистика по контенту:
  - Всего статей
  - Approval rate
  - Среднее время модерации
  - Топ категорий
- Графики:
  - Статьи по дням (created/approved/rejected/published)
  - По источникам
  - По категориям
- Таблица источников с метриками

**Компоненты:**
- ContentMetrics
- ArticlesChart
- SourceMetricsTable
- CategoryBreakdown

**API:**
- `GET /api/v1/analytics/dashboard/content`
- `GET /api/v1/content/sources`

---

#### 8.3 Funnel Analytics (`/analytics/funnels`)
**Функции:**
- Статистика по воронкам:
  - Всего воронок
  - Средняя конверсия
  - Всего входов
  - Всего завершений
- График воронки (funnel chart)
- Топ воронок по конверсии
- Детали по каждой воронке

**Компоненты:**
- FunnelMetrics
- FunnelChart
- TopFunnelsTable
- FunnelDetailsModal

**API:**
- `GET /api/v1/analytics/dashboard/funnels`
- `GET /api/v1/funnels/funnels`

---

#### 8.4 Broadcast Analytics (`/analytics/broadcasts`)
**Функции:**
- Статистика по рассылкам:
  - Всего рассылок
  - Средний delivery rate
  - Всего сообщений
- График доставок по времени
- Топ рассылок по доставке
- Ошибки доставки

**Компоненты:**
- BroadcastMetrics
- DeliveryChart
- BroadcastsTable
- DeliveryErrorsList

**API:**
- `GET /api/v1/analytics/dashboard/broadcasts`
- `GET /api/v1/funnels/broadcasts`

---

#### 8.5 Promotion Analytics (`/analytics/promotion`)
**Функции:**
- Статистика по продвижению:
  - Всего задач
  - Спаршено пользователей
  - Инвайчено пользователей
  - Масслукинг действий
  - Комментариев
- График по дням
- Топ задач по эффективности
- Ошибки инвайтинга

**Компоненты:**
- PromotionMetrics
- PromotionChart
- TasksTable
- InviteErrorsList

**API:**
- `GET /api/v1/analytics/dashboard/promotion`
- `GET /api/v1/promotion/tasks`

---

#### 8.6 AI Usage (`/analytics/ai`)
**Функции:**
- Статистика использования AI:
  - Всего запросов
  - Токенов использовано
  - По провайдерам (OpenAI, Anthropic, Ollama)
  - По операциям (rewrite, summarize, classify)
- График запросов по дням
- Топ проектов по использованию
- Estimated cost

**Компоненты:**
- AIUsageMetrics
- AIRequestsChart
- ProviderBreakdown
- OperationBreakdown
- CostEstimate

**API:**
- `GET /api/v1/ai/usage`
- `GET /api/v1/ai/requests`

---

### 9. Settings Module

#### 9.1 Profile Settings (`/settings/profile`)
**Функции:**
- Редактирование профиля:
  - First name
  - Last name
  - Email
  - Avatar (загрузка)
- Смена пароля
- Привязка Telegram:
  - Статус привязки
  - Кнопка привязать/отвязать
- Двухфакторная аутентификация

**Компоненты:**
- ProfileForm
- AvatarUploader
- ChangePasswordForm
- TelegramLinking
- TwoFASettings

**API:**
- `GET /api/v1/auth/me`
- `PATCH /api/v1/auth/me`
- `PATCH /api/v1/auth/me/password`
- `POST /api/v1/auth/telegram/link`

---

#### 9.2 Project Settings (`/settings/projects/:id`)
**Функции:**
- Настройки проекта:
  - Название
  - Slug
  - Описание
  - Логотип
- Члены проекта:
  - Список участников
  - Роли (admin, editor, analyst, operator, user)
  - Добавить участника (по email)
  - Изменить роль
  - Удалить участника
- Настройки проекта:
  - Timezone
  - Язык
  - Уведомления
- Опасная зона:
  - Деактивировать проект
  - Удалить проект

**Компоненты:**
- ProjectForm
- MembersList
- AddMemberModal
- RoleSelector
- ProjectSettingsForm
- DangerZone

**API:**
- `GET /api/v1/auth/projects/{id}`
- `PATCH /api/v1/auth/projects/{id}`
- `POST /api/v1/auth/projects/{id}/members`
- `DELETE /api/v1/auth/projects/{id}/members/{user_id}`

---

#### 9.3 API Keys (`/settings/api-keys`)
**Функции:**
- Список API ключей
- Создание нового ключа:
  - Название
  - Срок действия
  - Разрешения (scopes)
- Копирование ключа (только один раз)
- Отзыв ключа
- Лог использования ключей

**Компоненты:**
- APIKeysList
- CreateAPIKeyModal
- APIKeyScopesSelector
- APIKeyUsageLog

**API:**
- `GET /api/v1/auth/api-keys`
- `POST /api/v1/auth/api-keys`
- `DELETE /api/v1/auth/api-keys/{id}`

---

#### 9.4 Notifications Settings (`/settings/notifications`)
**Функции:**
- Настройки уведомлений:
  - Email уведомления
  - Telegram уведомления
  - Push уведомления
- События для уведомлений:
  - Статья одобрена/отклонена
  - Публикация успешна/неудачна
  - Рассылка завершена
  - Задача продвижения завершена
  - Ошибка в работе сервиса
- Расписание дайджестов

**Компоненты:**
- NotificationSettingsForm
- NotificationEventsList
- DigestSchedule

**API:**
- `GET /api/v1/auth/me/notifications`
- `PATCH /api/v1/auth/me/notifications`

---

### 10. Bot Interface

#### 10.1 Bot Commands (`/bot/commands`)
**Функции:**
- Список команд бота
- Редактирование команд:
  - Команда (/start, /help, etc.)
  - Описание
  - Действие
- Предпросмотр команд в Telegram

**Компоненты:**
- CommandsList
- CommandEditor
- TelegramPreview

**API:**
- `GET /api/v1/bot/commands`
- `PATCH /api/v1/bot/commands`

---

#### 10.2 Bot Messages (`/bot/messages`)
**Функции:**
- Шаблоны сообщений бота
- Редактор сообщений:
  - Текст
  - Кнопки (inline, reply)
  - Медиа (фото, видео)
- Тестирование сообщений

**Компоненты:**
- MessagesTemplates
- MessageEditor
- ButtonsBuilder
- MessageTest

**API:**
- `GET /api/v1/bot/messages`
- `POST /api/v1/bot/messages`

---

## 🔔 Уведомления (Toast/Notifications)

**Типы уведомлений:**
- ✅ Success — операция успешна
- ⚠️ Warning — предупреждение
- ❌ Error — ошибка
- ℹ️ Info — информация

**События для уведомлений:**
- Вход/выход из системы
- Сохранение настроек
- Запуск задачи
- Завершение задачи
- Ошибка API
- Истечение сессии

---

## 🎨 UI Components Library

### Базовые компоненты
- Button (primary, secondary, danger, ghost)
- Input (text, password, email, number, textarea)
- Select
- Checkbox
- Radio
- Switch/Toggle
- DatePicker
- TimePicker
- FileUpload
- ImageUpload
- Modal/Dialog
- Drawer/Sidebar
- Dropdown
- Tabs
- Accordion
- Tooltip
- Popover
- Badge
- Avatar
- Card
- Table
- Pagination
- Breadcrumbs
- Progress Bar
- Spinner/Loader
- Alert/Message
- Toast
- Skeleton Loader

### Специализированные компоненты
- RichTextEditor
- CodeEditor
- Chart (line, bar, pie, funnel)
- Calendar
- KanbanBoard
- TreeView
- SearchableSelect
- TagsInput
- ColorPicker
- CronEditor
- JSONEditor

---

## 📱 Responsive Design

**Breakpoints:**
- Mobile: < 576px
- Tablet: 576px - 768px
- Desktop: 768px - 992px
- Large Desktop: > 992px

**Адаптивность:**
- Sidebar сворачивается в hamburger menu на mobile
- Таблицы становятся scrollable или card view
- Формы перестраиваются в одну колонку
- Графики масштабируются

---

## ♿ Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus indicators
- Color contrast (WCAG AA)
- Screen reader support
- Skip to content link

---

## 🚀 Performance

- Code splitting by route
- Lazy loading components
- Image optimization
- API response caching
- Debounced search
- Virtual scrolling for large lists
- Service Worker for offline support

---

*Документ обновлён: 12 марта 2026*
