"""empty message

Revision ID: 87bd2e84e1d3
Revises: 02b97024942c
Create Date: 2025-01-30 15:15:27.567768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '87bd2e84e1d3'
down_revision = '02b97024942c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Events', schema=None) as batch_op:
        batch_op.alter_column('event_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Events', schema=None) as batch_op:
        batch_op.alter_column('event_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###
