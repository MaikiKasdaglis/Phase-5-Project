"""message

Revision ID: 33a3a8efdd76
Revises: 52cfff0f2525
Create Date: 2023-09-08 18:12:21.378327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33a3a8efdd76'
down_revision = '52cfff0f2525'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('months_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('month_total_credits', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('month_total_credits_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('month_total_pay', sa.Float(), nullable=True))

    with op.batch_alter_table('years_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year_total_credits', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_total_credits_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_total_pay', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('years_table', schema=None) as batch_op:
        batch_op.drop_column('year_total_pay')
        batch_op.drop_column('year_total_credits_rated')
        batch_op.drop_column('year_total_credits')

    with op.batch_alter_table('months_table', schema=None) as batch_op:
        batch_op.drop_column('month_total_pay')
        batch_op.drop_column('month_total_credits_rated')
        batch_op.drop_column('month_total_credits')

    # ### end Alembic commands ###
