"""create userbot tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-11

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enums first using raw SQL with exception handling
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE accountstatus AS ENUM ('inactive', 'active', 'banned', 'needs_auth', 'needs_2fa');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE proxytype AS ENUM ('mtproto', 'socks5', 'http');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create userbot_accounts table using raw SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS userbot_accounts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20),
            telegram_id BIGINT,
            username VARCHAR(100),
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            status accountstatus NOT NULL DEFAULT 'needs_auth',
            auth_phone VARCHAR(20),
            auth_code_hash VARCHAR(255),
            phone_code_hash VARCHAR(255),
            two_fa_password VARCHAR(255),
            session_string TEXT,
            is_warming_enabled BOOLEAN NOT NULL DEFAULT FALSE,
            warming_day INTEGER NOT NULL DEFAULT 0,
            warming_started_at TIMESTAMPTZ,
            last_warming_at TIMESTAMPTZ,
            is_online BOOLEAN NOT NULL DEFAULT FALSE,
            last_seen_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_userbot_accounts_project_id', 'userbot_accounts', ['project_id'], unique=False)
    op.create_index('ix_userbot_accounts_telegram_id', 'userbot_accounts', ['telegram_id'], unique=True)

    # Create proxies table using raw SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS proxies (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            account_id UUID NOT NULL,
            name VARCHAR(255) NOT NULL,
            proxy_type proxytype NOT NULL,
            hostname VARCHAR(255) NOT NULL,
            port INTEGER NOT NULL,
            username VARCHAR(255),
            password VARCHAR(255),
            secret VARCHAR(255),
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            is_working BOOLEAN,
            last_checked_at TIMESTAMPTZ,
            response_time_ms INTEGER,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_proxies_account_id', 'proxies', ['account_id'], unique=False)

    # Create session_data table using raw SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS session_data (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            account_id UUID NOT NULL UNIQUE,
            encrypted_session TEXT NOT NULL,
            dc_id INTEGER,
            server VARCHAR(255),
            port INTEGER,
            is_valid BOOLEAN NOT NULL DEFAULT TRUE,
            expires_at TIMESTAMPTZ,
            last_used_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_session_data_account_id', 'session_data', ['account_id'], unique=True)


def downgrade() -> None:
    op.drop_table('session_data')
    op.drop_table('proxies')
    op.drop_table('userbot_accounts')
    op.execute("DROP TYPE IF EXISTS accountstatus")
    op.execute("DROP TYPE IF EXISTS proxytype")
