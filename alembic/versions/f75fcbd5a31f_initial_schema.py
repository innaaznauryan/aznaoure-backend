"""initial_schema

Revision ID: f75fcbd5a31f
Revises: 
Create Date: 2026-06-29 23:44:49.778312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f75fcbd5a31f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('products',
                    sa.Column('id', sa.String(length=100), nullable=False),
                    sa.Column('name', sa.JSON(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('category', sa.Enum('rings', 'necklaces', 'earrings', 'bracelets', 'brooches',
                                                  name='productcategory'), nullable=False),
                    sa.Column('image', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.JSON(), nullable=False),
                    sa.Column('details', sa.JSON(), nullable=False),
                    sa.Column('available', sa.Boolean(), nullable=False),
                    sa.Column('featured', sa.Boolean(), nullable=False),
                    sa.Column('favorite', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('hashed_password', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=100), nullable=False),
                    sa.Column('last_name', sa.String(length=100), nullable=False),
                    sa.Column('phone', sa.String(length=50), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    op.create_table('orders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('phone', sa.String(length=50), nullable=True),
                    sa.Column('first_name', sa.String(length=100), nullable=False),
                    sa.Column('last_name', sa.String(length=100), nullable=False),
                    sa.Column('address', sa.String(length=255), nullable=False),
                    sa.Column('city', sa.String(length=100), nullable=False),
                    sa.Column('zip_code', sa.String(length=20), nullable=False),
                    sa.Column('country', sa.String(length=100), nullable=False),
                    sa.Column('subtotal', sa.Integer(), nullable=False),
                    sa.Column('shipping_cost', sa.Integer(), nullable=False),
                    sa.Column('total_amount', sa.Integer(), nullable=False),
                    sa.Column('status',
                              sa.Enum('pending', 'confirmed', 'shipped', 'delivered', 'cancelled', name='orderstatus'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)

    op.create_table('order_items',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.String(length=100), nullable=False),
                    sa.Column('product_name', sa.String(length=255), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.Column('unit_price', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)

    op.create_table('addresses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('phone', sa.String(length=50), nullable=True),
                    sa.Column('address', sa.String(length=255), nullable=False),
                    sa.Column('city', sa.String(length=100), nullable=False),
                    sa.Column('zip_code', sa.String(length=20), nullable=False),
                    sa.Column('country', sa.String(length=100), nullable=False),
                    sa.Column('is_default', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_addresses_id'), 'addresses', ['id'], unique=False)
    op.create_index(op.f('ix_addresses_user_id'), 'addresses', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('addresses')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('products')
    op.execute('DROP TYPE IF EXISTS productcategory')
    op.execute('DROP TYPE IF EXISTS orderstatus')