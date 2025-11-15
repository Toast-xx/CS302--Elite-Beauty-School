"""Add active field to users

Revision ID: 49b6dc271363
Revises: badaa70ac18a
Create Date: 2025-11-15 23:48:03.444471

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '49b6dc271363'
down_revision = 'badaa70ac18a'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the column as nullable
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=True))
    # Step 2: Set all existing users to active=True
    op.execute("UPDATE users SET active = TRUE")
    # Step 3: Alter the column to be NOT NULL
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('active', nullable=False)

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('active')