"""empty message

Revision ID: 77dfb03be148
Revises: 741cf562cd0c
Create Date: 2025-04-06 12:04:17.970197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77dfb03be148'
down_revision = '741cf562cd0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exam_completions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('attempt_number', sa.Integer(), nullable=False),
    sa.Column('completion_status', sa.String(length=50), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['Exams.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exam_completions')
    # ### end Alembic commands ###
