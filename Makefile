# ===========================================
# TeleFlow Platform — Makefile
# ===========================================

.PHONY: help up down restart logs ps migrate test lint format build pull clean dev

# Docker Compose command (v2 uses 'docker compose' instead of 'docker-compose')
DC = docker compose

# -------------------------------------------
# Основные команды
# -------------------------------------------

help: ## Показать эту справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Запустить все сервисы (detached mode)
	$(DC) up -d

up-build: ## Запустить все сервисы с пересборкой
	$(DC) up -d --build

up-dev: ## Запустить в режиме разработки (с логами)
	$(DC) up

down: ## Остановить все сервисы
	$(DC) down

restart: ## Перезапустить все сервисы
	$(DC) restart

ps: ## Показать статус сервисов
	$(DC) ps

logs: ## Показать логи всех сервисов
	$(DC) logs -f

logs-service: ## Показать логи конкретного сервиса (make logs-service SERVICE=auth-service)
	$(DC) logs -f $(SERVICE)

# -------------------------------------------
# Миграции
# -------------------------------------------

migrate: ## Запустить миграции всех сервисов
	@echo "Running migrations..."
	@for service in services/*; do \
		if [ -d "$$service/alembic" ]; then \
			echo "Migrating $$service..."; \
			$(DC) exec -T $$(basename $$service) alembic upgrade head || true; \
		fi; \
	done

migrate-service: ## Запустить миграции конкретного сервиса (make migrate-service SERVICE=auth-service)
	$(DC) exec $(SERVICE) alembic upgrade head

# -------------------------------------------
# Тесты и линтинг
# -------------------------------------------

test: ## Запустить все тесты
	@echo "Running tests..."
	@for service in services/*; do \
		if [ -d "$$service/tests" ]; then \
			echo "Testing $$service..."; \
			$(DC) exec -T $$(basename $$service) pytest || true; \
		fi; \
	done

test-service: ## Запустить тесты конкретного сервиса (make test-service SERVICE=auth-service)
	$(DC) exec $(SERVICE) pytest

lint: ## Запустить линтинг (ruff)
	@echo "Running linter..."
	@for service in services/*; do \
		if [ -f "$$service/requirements.txt" ]; then \
			echo "Linting $$service..."; \
			$(DC) exec -T $$(basename $$service) ruff check . || true; \
		fi; \
	done
	$(DC) exec -T shared ruff check . || true

format: ## Отформатировать код (black + isort)
	@echo "Formatting code..."
	@for service in services/*; do \
		if [ -f "$$service/requirements.txt" ]; then \
			echo "Formatting $$service..."; \
			$(DC) exec -T $$(basename $$service) black . || true; \
			$(DC) exec -T $$(basename $$service) isort . || true; \
		fi; \
	done

# -------------------------------------------
# Docker
# -------------------------------------------

build: ## Собрать все образы
	$(DC) build

build-service: ## Собрать образ конкретного сервиса (make build-service SERVICE=auth-service)
	$(DC) build $(SERVICE)

pull: ## Скачать все образы
	$(DC) pull

clean: ## Очистить всё (volumes, images, cache)
	$(DC) down -v --rmi all --remove-orphans
	docker system prune -f

# -------------------------------------------
# Разработка
# -------------------------------------------

dev: ## Режим разработки: up + логи
	$(DC) up -d
	$(DC) logs -f

shell: ## Получить shell в сервисе (make shell SERVICE=auth-service)
	$(DC) exec $(SERVICE) /bin/bash

db: ## Подключиться к PostgreSQL
	$(DC) exec postgres psql -U teleflow -d teleflow

redis: ## Подключиться к Redis CLI
	$(DC) exec redis redis-cli

# -------------------------------------------
# Shared library
# -------------------------------------------

install-shared: ## Установить teleflow-common локально для разработки
	pip install -e shared/teleflow-common

publish-shared: ## Собрать и опубликовать teleflow-common (для production)
	cd shared/teleflow-common && poetry build && poetry publish
