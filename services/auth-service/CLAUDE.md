# Auth Service — AI Context

## Responsibility

Authentication, authorization, user management, projects, and RBAC.

## Database: auth_db

### Tables

- `users` — User accounts
- `projects` — Multi-tenant projects
- `project_members` — User-project membership with roles
- `audit_logs` — Audit trail for all actions
- `token_blacklist` — Blacklisted refresh tokens (Redis in dev)

## Key Flows

1. **Registration**: Email/password → hash password → create user → send verification email
2. **Login**: Email/password → verify → JWT access + refresh tokens
3. **Token Refresh**: Refresh token → validate → new access + refresh tokens
4. **RBAC Check**: Request → extract JWT → validate → check permissions → allow/deny

## API Endpoints

```
POST   /api/v1/auth/register            — регистрация
POST   /api/v1/auth/login               — вход
POST   /api/v1/auth/refresh             — обновление токенов
POST   /api/v1/auth/logout              — выход
GET    /api/v1/auth/me                  — текущий профиль
PATCH  /api/v1/auth/me                  — обновление профиля

GET    /api/v1/auth/users               — список пользователей (admin)
GET    /api/v1/auth/users/{id}          — пользователь по ID (admin)
PATCH  /api/v1/auth/users/{id}/role     — изменение роли (admin)

POST   /api/v1/auth/projects            — создание проекта
GET    /api/v1/auth/projects            — список проектов
POST   /api/v1/auth/projects/{id}/members — добавление участника
```

## Events Published

- `user.created` {user_id, email}
- `user.logged_in` {user_id, timestamp}
- `project.created` {project_id, owner_id}
- `project.member_added` {project_id, user_id, role}

## Events Consumed

- None (auth is foundational service)

## Dependencies

- PostgreSQL (auth_db)
- Redis (token blacklist)
- teleflow-common (shared library)

## Internal Endpoints (service-to-service)

```
POST   /internal/auth/validate-token    — валидация токена
GET    /internal/auth/users/{id}        — данные пользователя
```
