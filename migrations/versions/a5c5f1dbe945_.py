"""empty message

Revision ID: a5c5f1dbe945
Revises: bac709280da0
Create Date: 2018-12-09 14:55:34.266499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5c5f1dbe945'
down_revision = 'bac709280da0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_personal', 'head_img')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_personal', sa.Column('head_img', sa.BLOB(), nullable=True))
    # ### end Alembic commands ###
