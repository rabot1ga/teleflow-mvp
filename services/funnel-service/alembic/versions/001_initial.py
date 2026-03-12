"""Initial migration - create funnel tables

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15 13:00:00.000000

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
    # Create funnels table
    op.create_table(
        'funnels',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('trigger_type', sa.String(50), nullable=False),
        sa.Column('trigger_value', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_funnels_project_id'), 'funnels', ['project_id'], unique=False)

    # Create funnel_steps table
    op.create_table(
        'funnel_steps',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('funnel_id', sa.String(36), nullable=False),
        sa.Column('step_order', sa.Integer, nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('delay_type', sa.String(20), nullable=False, default='immediate'),
        sa.Column('delay_value', sa.Integer, nullable=True),
        sa.Column('delay_time', sa.String(50), nullable=True),
        sa.Column('condition', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('actions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('on_condition_fail', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['funnel_id'], ['funnels.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_funnel_steps_funnel_id'), 'funnel_steps', ['funnel_id'], unique=False)

    # Create funnel_users table
    op.create_table(
        'funnel_users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('funnel_id', sa.String(36), nullable=False),
        sa.Column('telegram_user_id', sa.BigInteger, nullable=False),
        sa.Column('current_step_id', sa.String(36), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, default='active'),
        sa.Column('user_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=False, default=list),
        sa.Column('source', sa.String(255), nullable=True),
        sa.Column('entered_at', sa.DateTime, nullable=False),
        sa.Column('last_action_at', sa.DateTime, nullable=True),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('next_step_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['funnel_id'], ['funnels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['current_step_id'], ['funnel_steps.id'], ondelete='SET NULL'),
    )
    op.create_index(op.f('ix_funnel_users_funnel_id'), 'funnel_users', ['funnel_id'], unique=False)
    op.create_index(op.f('ix_funnel_users_telegram_user_id'), 'funnel_users', ['telegram_user_id'], unique=False)
    op.create_index(op.f('ix_funnel_users_next_step_at'), 'funnel_users', ['next_step_at'], unique=False)

    # Create lead_magnets table
    op.create_table(
        'lead_magnets',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('file_id', sa.String(255), nullable=True),
        sa.Column('file_path', sa.Text, nullable=True),
        sa.Column('url', sa.Text, nullable=True),
        sa.Column('text_content', sa.Text, nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('delivery_message', sa.Text, nullable=False),
        sa.Column('require_subscription', sa.Boolean, nullable=False, default=True),
        sa.Column('subscription_channel_id', sa.BigInteger, nullable=True),
        sa.Column('stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_lead_magnets_project_id'), 'lead_magnets', ['project_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_lead_magnets_project_id'), table_name='lead_magnets')
    op.drop_table('lead_magnets')
    op.drop_index(op.f('ix_funnel_users_next_step_at'), table_name='funnel_users')
    op.drop_index(op.f('ix_funnel_users_telegram_user_id'), table_name='funnel_users')
    op.drop_index(op.f('ix_funnel_users_funnel_id'), table_name='funnel_users')
    op.drop_table('funnel_users')
    op.drop_index(op.f('ix_funnel_steps_funnel_id'), table_name='funnel_steps')
    op.drop_table('funnel_steps')
    op.drop_index(op.f('ix_funnels_project_id'), table_name='funnels')
    op.drop_table('funnels')
