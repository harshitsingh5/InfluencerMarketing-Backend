"""empty message

Revision ID: 92cea535fbda
Revises: ca8a88f29652
Create Date: 2019-08-18 11:58:41.702337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '92cea535fbda'
down_revision = 'ca8a88f29652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaign', sa.Column('image', sa.String(length=30), nullable=True))
    op.drop_column('campaign', 'typeC')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaign', sa.Column('typeC', mysql.VARCHAR(length=30), nullable=True))
    op.drop_column('campaign', 'image')
    # ### end Alembic commands ###
