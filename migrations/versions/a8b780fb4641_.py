"""empty message

Revision ID: a8b780fb4641
Revises: 16e20e71fce5
Create Date: 2019-08-25 19:40:34.231269

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a8b780fb4641'
down_revision = '16e20e71fce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('influencers_involved', sa.Column('range_type', sa.Integer(), nullable=True))
    op.drop_column('pricing_details', 'follower_range')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pricing_details', sa.Column('follower_range', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('influencers_involved', 'range_type')
    # ### end Alembic commands ###