"""empty message

Revision ID: 0588823c3cdc
Revises: 
Create Date: 2020-02-01 21:00:55.691435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0588823c3cdc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=80), nullable=False))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
