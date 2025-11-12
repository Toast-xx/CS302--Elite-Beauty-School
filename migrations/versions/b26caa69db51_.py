"""empty message

Revision ID: b26caa69db51
Revises: 1f01a78e625a
Create Date: 2025-10-22 00:54:52.391794

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b26caa69db51'
down_revision = '1f01a78e625a'
branch_labels = None
depends_on = None

def upgrade():
    # Make campus_products.price NOT NULL
    with op.batch_alter_table('campus_products', schema=None) as batch_op:
        batch_op.alter_column('price', type_=sa.Numeric(10, 2), nullable=False)

    # Add campus_product_id to order_items (do NOT add price column again)
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('campus_product_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'campus_products', ['campus_product_id'], ['id'])
       
    # Set price to NOT NULL and remove default (only alter, do not add)
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.alter_column('price', nullable=False, server_default=None)

    # Drop quantity from products
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('quantity')

def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True))

    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.drop_column('price')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('campus_product_id')

    with op.batch_alter_table('campus_products', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)