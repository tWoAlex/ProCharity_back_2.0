"""archive to is_archived

Revision ID: ff7829853115
Revises: bb02384217e4
Create Date: 2023-05-18 18:20:06.480663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff7829853115'
down_revision = 'bb02384217e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('is_archived', sa.Boolean(), nullable=False))
    op.drop_column('categories', 'archive')
    op.add_column('tasks', sa.Column('is_archived', sa.Boolean(), nullable=False))
    op.drop_column('tasks', 'archive')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('archive', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('tasks', 'is_archived')
    op.add_column('categories', sa.Column('archive', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('categories', 'is_archived')
    # ### end Alembic commands ###