"""Add moderation tables

Revision ID: 002_moderation
Revises: 001_initial
Create Date: 2024-01-15 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002_moderation'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create moderation_batches table
    op.create_table(
        'moderation_batches',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('moderator_id', sa.String(36), nullable=True),
        sa.Column('strategy', sa.String(50), nullable=False, default='by_priority'),
        sa.Column('article_ids', postgresql.ARRAY(sa.String(36)), nullable=False),
        sa.Column('telegram_message_ids', postgresql.ARRAY(sa.BigInteger), nullable=False, default=list),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_moderation_batches_project_id'), 'moderation_batches', ['project_id'], unique=False)

    # Create automation_rules table
    op.create_table(
        'automation_rules',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('priority', sa.Integer, nullable=False, default=0),
        sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('actions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_automation_rules_project_id'), 'automation_rules', ['project_id'], unique=False)

    # Add moderation_batch_id to articles table
    op.add_column('articles', sa.Column('moderation_batch_id', sa.String(36), nullable=True))
    op.create_foreign_key(
        'fk_articles_moderation_batch_id',
        'articles', 'moderation_batches',
        ['moderation_batch_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_articles_moderation_batch_id', 'articles', type_='foreignkey')
    op.drop_column('articles', 'moderation_batch_id')
    op.drop_index(op.f('ix_automation_rules_project_id'), table_name='automation_rules')
    op.drop_table('automation_rules')
    op.drop_index(op.f('ix_moderation_batches_project_id'), table_name='moderation_batches')
    op.drop_table('moderation_batches')
