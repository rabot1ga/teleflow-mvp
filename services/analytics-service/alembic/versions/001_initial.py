"""create analytics tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-12

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create analytics_events table
    op.execute("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            event_type VARCHAR(100) NOT NULL,
            entity_type VARCHAR(50),
            entity_id UUID,
            payload JSONB,
            user_id UUID,
            event_timestamp TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_analytics_events_project_id', 'analytics_events', ['project_id'], unique=False)
    op.create_index('ix_analytics_events_event_type', 'analytics_events', ['event_type'], unique=False)
    op.create_index('ix_analytics_events_entity_id', 'analytics_events', ['entity_id'], unique=False)
    op.create_index('ix_analytics_events_user_id', 'analytics_events', ['user_id'], unique=False)
    op.create_index('ix_analytics_events_timestamp', 'analytics_events', ['event_timestamp'], unique=False)

    # Create analytics_daily table
    op.execute("""
        CREATE TABLE IF NOT EXISTS analytics_daily (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            articles_created INTEGER NOT NULL DEFAULT 0,
            articles_approved INTEGER NOT NULL DEFAULT 0,
            articles_rejected INTEGER NOT NULL DEFAULT 0,
            articles_published INTEGER NOT NULL DEFAULT 0,
            funnel_entries INTEGER NOT NULL DEFAULT 0,
            funnel_completions INTEGER NOT NULL DEFAULT 0,
            broadcasts_sent INTEGER NOT NULL DEFAULT 0,
            messages_delivered INTEGER NOT NULL DEFAULT 0,
            users_parsed INTEGER NOT NULL DEFAULT 0,
            users_invited INTEGER NOT NULL DEFAULT 0,
            userbot_actions INTEGER NOT NULL DEFAULT 0,
            ai_requests INTEGER NOT NULL DEFAULT 0,
            ai_tokens_used INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_analytics_daily_project_id', 'analytics_daily', ['project_id'], unique=False)
    op.create_index('ix_analytics_daily_date', 'analytics_daily', ['date'], unique=False)


def downgrade() -> None:
    op.drop_table('analytics_daily')
    op.drop_table('analytics_events')
