"""message

Revision ID: bdc22e2892aa
Revises: 7cf90bf59e28
Create Date: 2023-09-07 16:13:23.499298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdc22e2892aa'
down_revision = '7cf90bf59e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('days_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('a_pay', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('days_table', schema=None) as batch_op:
        batch_op.drop_column('a_pay')

    # ### end Alembic commands ###
