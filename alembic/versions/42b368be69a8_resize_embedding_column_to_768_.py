"""resize embedding column to 768 dimensions

Revision ID: 42b368be69a8
Revises: 3f7497c95c71
Create Date: 2026-09-09 15:52:16.956424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42b368be69a8'
down_revision: Union[str, Sequence[str], None] = '3f7497c95c71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE products SET embedding = NULL;")
    op.execute("ALTER TABLE products ALTER COLUMN embedding TYPE vector(768);")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE products SET embedding = NULL;")
    op.execute("ALTER TABLE products ALTER COLUMN embedding TYPE vector(384);")
    