"""empty message

Revision ID: 3f55b2d6e947
Revises: af1d1bd75fca
Create Date: 2018-11-24 20:03:35.628034

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3f55b2d6e947'
down_revision = 'af1d1bd75fca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_personal', 'password_hash',
               existing_type=mysql.VARCHAR(length=60),
               type_=sa.String(length=128),
               existing_nullable=False)
    op.alter_column('user_shop', 'password_hash',
               existing_type=mysql.VARCHAR(length=60),
               type_=sa.String(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_shop', 'password_hash',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=60),
               existing_nullable=False)
    op.alter_column('user_personal', 'password_hash',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=60),
               existing_nullable=False)
    # ### end Alembic commands ###
