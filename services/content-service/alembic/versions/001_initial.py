"""Initial migration - create content tables

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15 10:00:00.000000

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
    # Create sources table
    op.create_table(
        'sources',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('url', sa.Text, nullable=True),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=dict),
        sa.Column('fetch_interval_minutes', sa.Integer, nullable=False, default=30),
        sa.Column('default_category', sa.String(100), nullable=True),
        sa.Column('default_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=list),
        sa.Column('priority_boost', sa.Integer, nullable=False, default=0),
        sa.Column('reputation', sa.Float, nullable=False, default=0.5),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('last_fetch_at', sa.DateTime, nullable=True),
        sa.Column('last_error', sa.Text, nullable=True),
        sa.Column('error_count', sa.Integer, nullable=False, default=0),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sources_project_id'), 'sources', ['project_id'], unique=False)

    # Create source_runs table
    op.create_table(
        'source_runs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('source_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('articles_found', sa.Integer, nullable=False, default=0),
        sa.Column('articles_new', sa.Integer, nullable=False, default=0),
        sa.Column('articles_duplicate', sa.Integer, nullable=False, default=0),
        sa.Column('error', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_source_runs_source_id'), 'source_runs', ['source_id'], unique=False)

    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('source_id', sa.String(36), nullable=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('summary', sa.Text, nullable=True),
        sa.Column('url', sa.Text, nullable=True),
        sa.Column('image_url', sa.Text, nullable=True),
        sa.Column('image_path', sa.String(500), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, default=list),
        sa.Column('language', sa.String(10), nullable=False, default='ru'),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('quality_score', sa.Float, nullable=False, default=0.0),
        sa.Column('priority_score', sa.Integer, nullable=False, default=50),
        sa.Column('url_hash', sa.String(64), nullable=True),
        sa.Column('content_hash', sa.String(64), nullable=True),
        sa.Column('simhash', sa.BigInteger, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('moderated_by', sa.String(36), nullable=True),
        sa.Column('moderated_at', sa.DateTime, nullable=True),
        sa.Column('rejection_reason', sa.String(50), nullable=True),
        sa.Column('rejection_comment', sa.Text, nullable=True),
        sa.Column('published_at', sa.DateTime, nullable=True),
        sa.Column('publish_target_id', sa.String(36), nullable=True),
        sa.Column('telegram_message_id', sa.BigInteger, nullable=True),
        sa.Column('original_pub_date', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ondelete='SET NULL'),
    )
    op.create_index(op.f('ix_articles_project_id'), 'articles', ['project_id'], unique=False)
    op.create_index(op.f('ix_articles_source_id'), 'articles', ['source_id'], unique=False)
    op.create_index(op.f('ix_articles_status'), 'articles', ['status'], unique=False)
    op.create_index(op.f('ix_articles_category'), 'articles', ['category'], unique=False)
    op.create_index(op.f('ix_articles_url_hash'), 'articles', ['url_hash'], unique=True)
    op.create_index(op.f('ix_articles_content_hash'), 'articles', ['content_hash'], unique=False)

    # Create article_versions table
    op.create_table(
        'article_versions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('title', sa.Text, nullable=True),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('changed_by', sa.String(36), nullable=True),
        sa.Column('changed_at', sa.DateTime, nullable=False),
        sa.Column('change_type', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_article_versions_article_id'), 'article_versions', ['article_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_article_versions_article_id'), table_name='article_versions')
    op.drop_table('article_versions')
    op.drop_index(op.f('ix_articles_content_hash'), table_name='articles')
    op.drop_index(op.f('ix_articles_url_hash'), table_name='articles')
    op.drop_index(op.f('ix_articles_category'), table_name='articles')
    op.drop_index(op.f('ix_articles_status'), table_name='articles')
    op.drop_index(op.f('ix_articles_source_id'), table_name='articles')
    op.drop_index(op.f('ix_articles_project_id'), table_name='articles')
    op.drop_table('articles')
    op.drop_index(op.f('ix_source_runs_source_id'), table_name='source_runs')
    op.drop_table('source_runs')
    op.drop_index(op.f('ix_sources_project_id'), table_name='sources')
    op.drop_table('sources')
