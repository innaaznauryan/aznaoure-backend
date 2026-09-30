"""add others category to product enum

Revision ID: b5d9a3a82e58
Revises: a0342f63b3bf
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b5d9a3a82e58'
down_revision: Union[str, Sequence[str], None] = 'a0342f63b3bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE productcategory ADD VALUE IF NOT EXISTS 'others'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL does not support removing a value from an enum directly in-place.
    # Keeping this migration as a no-op avoids data loss for existing rows.
    pass
