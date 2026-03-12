"""Initial migration - create content tables

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # TODO: Create tables
    pass


def downgrade() -> None:
    # TODO: Drop tables
    pass
