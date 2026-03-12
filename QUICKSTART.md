# TeleFlow Platform — Быстрый старт

## Предварительные требования

- Docker и Docker Compose
- 4+ GB RAM
- 10+ GB свободного места на диске

## Установка

### 1. Клонирование и настройка

```bash
cd /root/Desktop/P1/teleflow

# Создать .env файл из примера
cp .env.example .env

# Изменить секреты в .env (обязательно!):
# - JWT_SECRET
# - POSTGRES_PASSWORD
# - TELEGRAM_BOT_TOKEN (если есть)
# - OPENAI_API_KEY (если используется AI)
```

### 2. Запуск инфраструктуры

```bash
# Запустить все сервисы
make up

# Или с пересборкой образов
make up-build

# Проверить статус
make ps

# Просмотр логов
make logs
```

### 3. Применение миграций

```bash
# Применить миграции для всех сервисов
make migrate
```

### 4. Проверка работы

```bash
# Проверить health auth-service
curl http://localhost/api/v1/auth/health

# Проверить health content-service
curl http://localhost/api/v1/content/health

# Открыть Swagger UI
# http://localhost/api/v1/auth/docs
```

## Сервисы и порты

| Сервис | URL | Порт |
|--------|-----|------|
| Traefik (Gateway) | http://localhost | 80 |
| Traefik Dashboard | http://traefik.localhost | 8080 |
| Frontend | http://localhost | 3000 |
| Auth Service | http://localhost/api/v1/auth | 8001 |
| Content Service | http://localhost/api/v1/content | 8002 |
| Publishing Service | http://localhost/api/v1/publishing | 8004 |
| Funnel Service | http://localhost/api/v1/funnels | 8005 |
| Bot Gateway | http://localhost/api/v1/bot | 8006 |
| Userbot Service | http://localhost/api/v1/userbot | 8007 |
| Promotion Service | http://localhost/api/v1/promotion | 8008 |
| AI Service | http://localhost/api/v1/ai | 8009 |
| Analytics Service | http://localhost/api/v1/analytics | 8010 |
| PostgreSQL | localhost | 5432 |
| Redis | localhost | 6379 |
| Meilisearch | http://localhost:7700 | 7700 |
| MinIO Console | http://localhost:9001 | 9001 |
| Prometheus | http://localhost:9090 | 9090 |
| Grafana | http://localhost:3001 | 3001 |
| Loki | http://localhost:3100 | 3100 |

## Основные команды Makefile

```bash
make up          # Запустить все сервисы
make down        # Остановить все сервисы
make restart     # Перезапустить все сервисы
make logs        # Показать логи всех сервисов
make logs-service SERVICE=auth-service  # Логи конкретного сервиса
make ps          # Статус сервисов
make migrate     # Применить миграции
make test        # Запустить тесты
make lint        # Запустить линтинг
make build       # Собрать все образы
make clean       # Очистить всё (volumes, images)
make shell SERVICE=auth-service  # Получить shell в сервисе
make db          # Подключиться к PostgreSQL
make redis       # Подключиться к Redis CLI
```

## Тестирование API

### Регистрация пользователя

```bash
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Вход

```bash
curl -X POST http://localhost/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

### Получить текущий профиль

```bash
curl http://localhost/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Разработка

### Добавление нового сервиса

1. Создать структуру в `services/<service-name>/`
2. Добавить сервис в `docker-compose.yml`
3. Добавить labels для Traefik routing
4. Создать БД в `infra/postgres/init-db.sh`

### Изменение shared library

```bash
# Установить в development режиме
make install-shared

# После изменений в teleflow-common
docker-compose restart <service-name>
```

## Отладка

### Просмотр логов конкретного сервиса

```bash
docker-compose logs -f auth-service
```

### Подключение к БД сервиса

```bash
make db
# \c content_db  -- переключиться на БД content
```

### Проверка миграций

```bash
docker-compose exec auth-service alembic current
docker-compose exec auth-service alembic history
```

## Production checklist

- [ ] Изменить все секреты в .env
- [ ] Настроить HTTPS для Traefik
- [ ] Включить аутентификацию для Traefik Dashboard
- [ ] Настроить backup для PostgreSQL
- [ ] Настроить alerting в Grafana
- [ ] Включить rate limiting в Traefik
- [ ] Настроить CORS для frontend
- [ ] Использовать Docker secrets для敏感 данных

## Проблемы и решения

### Ошибка "Connection refused" к PostgreSQL

Проверьте что БД создана:
```bash
docker-compose exec postgres psql -U teleflow -c "\l"
```

### Сервис не стартует

Проверьте логи:
```bash
make logs-service SERVICE=<service-name>
```

### Миграции не применяются

Проверьте подключение к БД:
```bash
docker-compose exec <service-name> alembic upgrade head
```

## Дополнительная документация

- [WORK.md](./WORK.md) — План разработки и прогресс
- [CLAUDE.md](./CLAUDE.md) — Контекст для AI
- [tz.md](./tz.md) — Полное техническое задание
