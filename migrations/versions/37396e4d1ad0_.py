"""empty message

Revision ID: 37396e4d1ad0
Revises: None
Create Date: 2016-08-14 20:13:03.334552

"""

# revision identifiers, used by Alembic.
revision = '37396e4d1ad0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    ### end Alembic commands ###
