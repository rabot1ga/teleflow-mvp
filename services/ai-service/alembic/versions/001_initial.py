"""create ai tables

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
    # Create ai_requests table (no enums - using strings)
    op.execute("""
        CREATE TABLE IF NOT EXISTS ai_requests (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            provider VARCHAR(50) NOT NULL,
            model VARCHAR(100) NOT NULL,
            operation VARCHAR(50) NOT NULL,
            input_text TEXT NOT NULL,
            output_text TEXT,
            parameters JSONB,
            input_tokens INTEGER,
            output_tokens INTEGER,
            latency_ms INTEGER,
            status VARCHAR(20) NOT NULL DEFAULT 'completed',
            error_message TEXT,
            is_cached BOOLEAN NOT NULL DEFAULT FALSE,
            cache_key VARCHAR(255),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_ai_requests_project_id', 'ai_requests', ['project_id'], unique=False)
    op.create_index('ix_ai_requests_cache_key', 'ai_requests', ['cache_key'], unique=False)

    # Create ai_usage table
    op.execute("""
        CREATE TABLE IF NOT EXISTS ai_usage (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            provider VARCHAR(50) NOT NULL,
            model VARCHAR(100) NOT NULL,
            total_requests INTEGER NOT NULL DEFAULT 0,
            successful_requests INTEGER NOT NULL DEFAULT 0,
            failed_requests INTEGER NOT NULL DEFAULT 0,
            cached_requests INTEGER NOT NULL DEFAULT 0,
            total_input_tokens INTEGER NOT NULL DEFAULT 0,
            total_output_tokens INTEGER NOT NULL DEFAULT 0,
            avg_latency_ms INTEGER,
            max_latency_ms INTEGER,
            estimated_cost DECIMAL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.create_index('ix_ai_usage_project_id', 'ai_usage', ['project_id'], unique=False)
    op.create_index('ix_ai_usage_date', 'ai_usage', ['date'], unique=False)


def downgrade() -> None:
    op.drop_table('ai_usage')
    op.drop_table('ai_requests')
