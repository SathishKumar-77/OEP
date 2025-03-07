"""New Course DB added

Revision ID: 6133c7053fb7
Revises: 1ecd85d09b46
Create Date: 2025-01-17 13:23:10.374305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6133c7053fb7'
down_revision = '1ecd85d09b46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('department_name', sa.String(length=100), nullable=False),
    sa.Column('year', sa.String(length=20), nullable=False),
    sa.Column('semester', sa.String(length=50), nullable=False),
    sa.Column('subjects', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course')
    # ### end Alembic commands ###
