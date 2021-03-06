"""empty message

Revision ID: 284f1d50a99e
Revises: 2c57824c4adc
Create Date: 2019-08-20 08:37:22.482883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '284f1d50a99e'
down_revision = '2c57824c4adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaign', sa.Column('creative_req', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaign', 'creative_req')
    # ### end Alembic commands ###
