"""test

Revision ID: abb2a580c603
Revises: 
Create Date: 2021-02-01 14:18:56.030038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abb2a580c603'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('newspapers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('year_of_fundation', sa.Integer(), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('director', sa.String(), nullable=True),
    sa.Column('orientation', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'nationality', name='_name_nationality_uc')
    )
    op.create_index(op.f('ix_newspapers_id'), 'newspapers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_newspapers_id'), table_name='newspapers')
    op.drop_table('newspapers')
    # ### end Alembic commands ###
