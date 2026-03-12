"""Initial migration - create publishing tables

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create publish_targets table
    op.create_table(
        'publish_targets',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('telegram_chat_id', sa.BigInteger, nullable=False),
        sa.Column('telegram_chat_title', sa.String(255), nullable=True),
        sa.Column('is_default', sa.Boolean, nullable=False, default=False),
        sa.Column('is_verified', sa.Boolean, nullable=False, default=False),
        sa.Column('min_interval_seconds', sa.Integer, nullable=False, default=300),
        sa.Column('max_per_hour', sa.Integer, nullable=False, default=6),
        sa.Column('max_per_day', sa.Integer, nullable=False, default=30),
        sa.Column('working_hours_start', sa.Time, nullable=True),
        sa.Column('working_hours_end', sa.Time, nullable=True),
        sa.Column('timezone', sa.String(50), nullable=False, default='Europe/Moscow'),
        sa.Column('categories', postgresql.ARRAY(sa.String()), nullable=False, default=list),
        sa.Column('default_template_id', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('last_published_at', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_publish_targets_project_id'), 'publish_targets', ['project_id'], unique=False)

    # Create publish_templates table
    op.create_table(
        'publish_templates',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('parse_mode', sa.String(10), nullable=False, default='HTML'),
        sa.Column('disable_preview', sa.Boolean, nullable=False, default=False),
        sa.Column('buttons', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=list),
        sa.Column('scope', sa.String(20), nullable=False, default='global'),
        sa.Column('scope_value', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_publish_templates_project_id'), 'publish_templates', ['project_id'], unique=False)

    # Create publish_jobs table
    op.create_table(
        'publish_jobs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('target_id', sa.String(36), nullable=False),
        sa.Column('template_id', sa.String(36), nullable=True),
        sa.Column('scheduled_at', sa.DateTime, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('telegram_message_id', sa.BigInteger, nullable=True),
        sa.Column('published_at', sa.DateTime, nullable=True),
        sa.Column('error', sa.Text, nullable=True),
        sa.Column('retry_count', sa.Integer, nullable=False, default=0),
        sa.Column('next_retry_at', sa.DateTime, nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['target_id'], ['publish_targets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['publish_templates.id'], ondelete='SET NULL'),
    )
    op.create_index(op.f('ix_publish_jobs_project_id'), 'publish_jobs', ['project_id'], unique=False)
    op.create_index(op.f('ix_publish_jobs_article_id'), 'publish_jobs', ['article_id'], unique=False)
    op.create_index(op.f('ix_publish_jobs_status'), 'publish_jobs', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_publish_jobs_status'), table_name='publish_jobs')
    op.drop_index(op.f('ix_publish_jobs_article_id'), table_name='publish_jobs')
    op.drop_index(op.f('ix_publish_jobs_project_id'), table_name='publish_jobs')
    op.drop_table('publish_jobs')
    op.drop_index(op.f('ix_publish_templates_project_id'), table_name='publish_templates')
    op.drop_table('publish_templates')
    op.drop_index(op.f('ix_publish_targets_project_id'), table_name='publish_targets')
    op.drop_table('publish_targets')
