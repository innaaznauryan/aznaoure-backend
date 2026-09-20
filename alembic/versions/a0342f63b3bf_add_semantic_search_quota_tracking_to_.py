"""add semantic search quota tracking to users

Revision ID: a0342f63b3bf
Revises: 42b368be69a8
Create Date: 2026-09-20 22:04:00.219562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0342f63b3bf'
down_revision: Union[str, Sequence[str], None] = '42b368be69a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE users ADD COLUMN semantic_search_count INTEGER NOT NULL DEFAULT 0"
    )
    op.execute(
        "ALTER TABLE users ADD COLUMN semantic_search_date DATE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE users DROP COLUMN semantic_search_date")
    op.execute("ALTER TABLE users DROP COLUMN semantic_search_count")
