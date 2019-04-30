"""Added name to user

Revision ID: f07bc8fefeee
Revises: 36d5d081b3cc
Create Date: 2019-04-30 00:33:47.960990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f07bc8fefeee'
down_revision = '36d5d081b3cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'class', ['join_code'])
    op.add_column('user', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    op.drop_constraint(None, 'class', type_='unique')
    # ### end Alembic commands ###