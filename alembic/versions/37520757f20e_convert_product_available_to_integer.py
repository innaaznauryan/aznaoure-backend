"""convert product available to integer

Revision ID: 37520757f20e
Revises: 7340bba3204a
Create Date: 2026-09-05 18:10:02.780549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37520757f20e'
down_revision: Union[str, Sequence[str], None] = '7340bba3204a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        ALTER TABLE products
        ALTER COLUMN available TYPE INTEGER
        USING (CASE WHEN available THEN 1 ELSE 0 END)
        """
    )
    op.alter_column(
        "products",
        "available",
        existing_type=sa.Integer(),
        nullable=False,
        server_default="0",
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        ALTER TABLE products
        ALTER
        COLUMN available TYPE BOOLEAN
        USING (available > 0)
        """
    )
    op.alter_column(
        "products",
        "available",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default="true",
    )
