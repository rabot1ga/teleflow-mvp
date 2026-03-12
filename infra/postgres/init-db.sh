#!/bin/bash
# ===========================================
# TeleFlow Platform — PostgreSQL Init Script
# ===========================================
# Создаёт все базы данных для микросервисов
# ===========================================

set -e

POSTGRES_USER="${POSTGRES_USER:-teleflow}"

echo "🚀 Creating databases for TeleFlow microservices..."

# Auth Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE auth_db;
    GRANT ALL PRIVILEGES ON DATABASE auth_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created auth_db"

# Content Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE content_db;
    GRANT ALL PRIVILEGES ON DATABASE content_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created content_db"

# Publishing Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE publish_db;
    GRANT ALL PRIVILEGES ON DATABASE publish_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created publish_db"

# Funnel Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE funnel_db;
    GRANT ALL PRIVILEGES ON DATABASE funnel_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created funnel_db"

# Bot Gateway
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE bot_db;
    GRANT ALL PRIVILEGES ON DATABASE bot_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created bot_db"

# Userbot Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE userbot_db;
    GRANT ALL PRIVILEGES ON DATABASE userbot_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created userbot_db"

# Promotion Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE promo_db;
    GRANT ALL PRIVILEGES ON DATABASE promo_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created promo_db"

# Analytics Service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE analytics_db;
    GRANT ALL PRIVILEGES ON DATABASE analytics_db TO $POSTGRES_USER;
EOSQL
echo "✅ Created analytics_db"

echo "🎉 All databases created successfully!"
