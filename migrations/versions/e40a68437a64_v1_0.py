"""v1.0

Revision ID: e40a68437a64
Revises: 
Create Date: 2018-12-03 16:15:55.575566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40a68437a64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_license',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('idcard_name', sa.String(length=30), nullable=True),
    sa.Column('idcard_num', sa.String(length=18), nullable=True),
    sa.Column('idcard_img', sa.LargeBinary(), nullable=True),
    sa.Column('business_img', sa.LargeBinary(), nullable=True),
    sa.Column('business_address', sa.String(length=100), nullable=True),
    sa.Column('business_name', sa.String(length=40), nullable=True),
    sa.Column('business_begin_time', sa.DateTime(), nullable=True),
    sa.Column('business_end_time', sa.DateTime(), nullable=True),
    sa.Column('business_num', sa.String(length=18), nullable=True),
    sa.Column('service_img', sa.LargeBinary(), nullable=True),
    sa.Column('service_address', sa.String(length=100), nullable=True),
    sa.Column('service_name', sa.String(length=40), nullable=True),
    sa.Column('service_begin_time', sa.DateTime(), nullable=True),
    sa.Column('service_end_time', sa.DateTime(), nullable=True),
    sa.Column('service_num', sa.String(length=18), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_num'),
    sa.UniqueConstraint('idcard_num'),
    sa.UniqueConstraint('service_num')
    )
    op.create_table('user_personal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('openid', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('head_img', sa.LargeBinary(length=2048), nullable=True),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('openid'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('user_shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('openid', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('openid'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('shop_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('shop_name', sa.String(length=30), nullable=False),
    sa.Column('shop_introduction', sa.Text(), nullable=True),
    sa.Column('contact_name', sa.String(length=30), nullable=False),
    sa.Column('contact_phone', sa.String(length=11), nullable=False),
    sa.Column('geocoding', sa.String(length=40), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('floor_send_cost', sa.Float(), nullable=True),
    sa.Column('send_cost', sa.Float(), nullable=True),
    sa.Column('notic', sa.String(length=200), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('shop_img', sa.LargeBinary(), nullable=True),
    sa.Column('box_price', sa.Float(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('license_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['license_id'], ['shop_license.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user_shop.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact_phone'),
    sa.UniqueConstraint('license_id'),
    sa.UniqueConstraint('owner_id'),
    sa.UniqueConstraint('shop_name')
    )
    op.create_table('user_address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('province', sa.String(length=20), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('district', sa.String(length=20), nullable=True),
    sa.Column('detail', sa.String(length=128), nullable=True),
    sa.Column('receiver_phone', sa.String(length=11), nullable=True),
    sa.Column('receiver_name', sa.String(length=20), nullable=True),
    sa.Column('geocoding', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('wx_order_no', sa.String(length=32), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('total_items', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_img', sa.LargeBinary(), nullable=True),
    sa.Column('item_stock', sa.Integer(), nullable=True),
    sa.Column('item_cate', sa.Integer(), nullable=True),
    sa.Column('item_price', sa.Integer(), nullable=True),
    sa.Column('item_introduction', sa.String(length=128), nullable=True),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_num', sa.Integer(), nullable=True),
    sa.Column('item_price', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_car',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_num', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_comment')
    op.drop_table('shopping_car')
    op.drop_table('order_items')
    op.drop_table('shop_items')
    op.drop_table('orders')
    op.drop_table('user_address')
    op.drop_table('shop_info')
    op.drop_table('user_shop')
    op.drop_table('user_personal')
    op.drop_table('shop_license')
    # ### end Alembic commands ###
