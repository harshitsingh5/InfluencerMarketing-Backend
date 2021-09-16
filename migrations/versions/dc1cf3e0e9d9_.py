"""empty message

Revision ID: dc1cf3e0e9d9
Revises: b877588894e4
Create Date: 2019-08-16 02:24:58.274698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc1cf3e0e9d9'
down_revision = 'b877588894e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('otp_details', sa.Column('otp_for', sa.Integer(), nullable=True))
    op.drop_column('otp_details', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('otp_details', sa.Column('type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('otp_details', 'otp_for')
    # ### end Alembic commands ###
