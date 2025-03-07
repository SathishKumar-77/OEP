"""empty message

Revision ID: 670af086757b
Revises: f2b7e5b1038c
Create Date: 2024-12-18 02:21:44.965556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670af086757b'
down_revision = 'f2b7e5b1038c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Question_Banks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('difficulty', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=500), nullable=False),
    sa.Column('option1', sa.String(length=500), nullable=False),
    sa.Column('option2', sa.String(length=500), nullable=False),
    sa.Column('option3', sa.String(length=500), nullable=False),
    sa.Column('option4', sa.String(length=500), nullable=False),
    sa.Column('question_bank_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_bank_id'], ['Question_Banks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Questions')
    op.drop_table('Question_Banks')
    # ### end Alembic commands ###
