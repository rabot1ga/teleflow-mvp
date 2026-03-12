"""create promotion tables

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
    # Create enums
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE promotiontasktype AS ENUM ('parse', 'invite', 'masslook', 'comment');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE promotiontaskstatus AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create promotion_tasks table
    op.execute("""
        CREATE TABLE IF NOT EXISTS promotion_tasks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            name VARCHAR(255) NOT NULL,
            task_type promotiontasktype NOT NULL,
            status promotiontaskstatus NOT NULL DEFAULT 'pending',
            config JSONB DEFAULT '{}',
            target_chat_id VARCHAR(100),
            target_chat_username VARCHAR(100),
            source_chat_id VARCHAR(100),
            source_chat_username VARCHAR(100),
            parse_filters JSONB,
            total_count INTEGER NOT NULL DEFAULT 0,
            processed_count INTEGER NOT NULL DEFAULT 0,
            success_count INTEGER NOT NULL DEFAULT 0,
            failed_count INTEGER NOT NULL DEFAULT 0,
            error_message TEXT,
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_promotion_tasks_project_id', 'promotion_tasks', ['project_id'], unique=False)

    # Create parsed_users table
    op.execute("""
        CREATE TABLE IF NOT EXISTS parsed_users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            task_id UUID NOT NULL,
            project_id UUID NOT NULL,
            telegram_id BIGINT NOT NULL,
            username VARCHAR(100),
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone VARCHAR(20),
            is_bot BOOLEAN NOT NULL DEFAULT FALSE,
            is_premium BOOLEAN NOT NULL DEFAULT FALSE,
            has_photo BOOLEAN NOT NULL DEFAULT FALSE,
            last_seen_days INTEGER,
            is_invited BOOLEAN NOT NULL DEFAULT FALSE,
            invited_at TIMESTAMPTZ,
            invite_error TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_parsed_users_task_id', 'parsed_users', ['task_id'], unique=False)
    op.create_index('ix_parsed_users_project_id', 'parsed_users', ['project_id'], unique=False)
    op.create_index('ix_parsed_users_telegram_id', 'parsed_users', ['telegram_id'], unique=False)
    op.create_index('ix_parsed_users_username', 'parsed_users', ['username'], unique=False)
    op.create_index('ix_parsed_users_is_invited', 'parsed_users', ['is_invited'], unique=False)


def downgrade() -> None:
    op.drop_table('parsed_users')
    op.drop_table('promotion_tasks')
    op.execute("DROP TYPE IF EXISTS promotiontasktype")
    op.execute("DROP TYPE IF EXISTS promotiontaskstatus")
