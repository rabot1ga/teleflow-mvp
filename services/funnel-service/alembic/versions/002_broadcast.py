"""Add broadcast and CRM tables

Revision ID: 002_broadcast
Revises: 001_initial
Create Date: 2024-01-15 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002_broadcast'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create broadcasts table
    op.create_table(
        'broadcasts',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('message_type', sa.String(20), nullable=False, default='text'),
        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('message_media_url', sa.Text, nullable=True),
        sa.Column('buttons', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('recipient_filter', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('scheduled_at', sa.DateTime, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, default='draft'),
        sa.Column('total_recipients', sa.Integer, nullable=False, default=0),
        sa.Column('sent', sa.Integer, nullable=False, default=0),
        sa.Column('delivered', sa.Integer, nullable=False, default=0),
        sa.Column('failed', sa.Integer, nullable=False, default=0),
        sa.Column('send_rate', sa.Integer, nullable=False, default=30),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('started_at', sa.DateTime, nullable=True),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_broadcasts_project_id'), 'broadcasts', ['project_id'], unique=False)
    op.create_index(op.f('ix_broadcasts_status'), 'broadcasts', ['status'], unique=False)

    # Create crm_segments table
    op.create_table(
        'crm_segments',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('user_count', sa.Integer, nullable=False, default=0),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_crm_segments_project_id'), 'crm_segments', ['project_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_crm_segments_project_id'), table_name='crm_segments')
    op.drop_table('crm_segments')
    op.drop_index(op.f('ix_broadcasts_status'), table_name='broadcasts')
    op.drop_index(op.f('ix_broadcasts_project_id'), table_name='broadcasts')
    op.drop_table('broadcasts')
