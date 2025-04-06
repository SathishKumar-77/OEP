"""empty message

Revision ID: 6b50e54eb146
Revises: d2c732d8cc0c
Create Date: 2025-04-06 05:09:30.607388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b50e54eb146'
down_revision = 'd2c732d8cc0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('selected_answer', sa.String(length=1), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['Exams.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['Questions.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['Student_Details.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Results')
    # ### end Alembic commands ###
