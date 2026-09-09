"""add embedding column to products

Revision ID: 3f7497c95c71
Revises: 37520757f20e
Create Date: 2026-09-07 12:41:14.941306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f7497c95c71'
down_revision: Union[str, Sequence[str], None] = '37520757f20e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # enable pgvector extension (safe to run even if already enabled)
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # add nullable embedding column, 384 dims to match the local
    # sentence-transformers model (paraphrase-multilingual-MiniLM-L12-v2)
    op.execute(
        "ALTER TABLE products ADD COLUMN embedding vector(384);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE products DROP COLUMN embedding;")
    # not dropping the extension on downgrade, other tables/migrations may rely on it