"""message

Revision ID: d879f3833faa
Revises: 804720ade328
Create Date: 2023-09-10 13:14:48.685204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd879f3833faa'
down_revision = '804720ade328'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('years_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year_tafb_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_int_tafb_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_tfp_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_vacation_sick_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_vja_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_vja_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_holiday_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_holiday_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_time_half_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_time_half_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_double_time_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_double_time_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_double_half_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_double_half_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_triple_rated', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_triple_pay', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('year_overrides_pay', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('year_a_pay', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('years_table', schema=None) as batch_op:
        batch_op.drop_column('year_a_pay')
        batch_op.drop_column('year_overrides_pay')
        batch_op.drop_column('year_triple_pay')
        batch_op.drop_column('year_triple_rated')
        batch_op.drop_column('year_double_half_pay')
        batch_op.drop_column('year_double_half_rated')
        batch_op.drop_column('year_double_time_pay')
        batch_op.drop_column('year_double_time_rated')
        batch_op.drop_column('year_time_half_pay')
        batch_op.drop_column('year_time_half_rated')
        batch_op.drop_column('year_holiday_pay')
        batch_op.drop_column('year_holiday_rated')
        batch_op.drop_column('year_vja_pay')
        batch_op.drop_column('year_vja_rated')
        batch_op.drop_column('year_vacation_sick_pay')
        batch_op.drop_column('year_tfp_pay')
        batch_op.drop_column('year_int_tafb_pay')
        batch_op.drop_column('year_tafb_pay')

    # ### end Alembic commands ###
