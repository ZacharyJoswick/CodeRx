"""Changed file storage schema

Revision ID: a119e83a7594
Revises: e1c11f032ce1
Create Date: 2019-04-28 19:20:15.449515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a119e83a7594'
down_revision = 'e1c11f032ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.drop_column('submission', 'new_field')
    op.drop_column('submission', 'files')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submission', sa.Column('files', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('submission', sa.Column('new_field', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_table('files',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('problem_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['problem_id'], ['problem.id'], name='files_problem_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='files_pkey')
    )
    # ### end Alembic commands ###