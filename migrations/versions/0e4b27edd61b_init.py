"""init

Revision ID: 0e4b27edd61b
Revises: 
Create Date: 2018-12-20 08:52:18.060272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e4b27edd61b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_default'), 'role', ['default'], unique=False)
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=True)
    op.create_table('user_personal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('openid', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('head_image_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('openid'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('user_shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=False),
    sa.Column('openid', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('head_image_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('openid'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('province', sa.Integer(), nullable=False),
    sa.Column('city', sa.Integer(), nullable=False),
    sa.Column('area', sa.Integer(), nullable=False),
    sa.Column('detailed', sa.String(length=64), nullable=False),
    sa.Column('contact_phone', sa.String(length=11), nullable=False),
    sa.Column('receiver', sa.String(length=20), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lng', sa.Float(), nullable=False),
    sa.Column('weights', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('admin_slat', sa.String(length=64), nullable=True),
    sa.Column('admin_phone', sa.Integer(), nullable=True),
    sa.Column('c_time', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('admin_phone')
    )
    op.create_index(op.f('ix_admin_name'), 'admin', ['name'], unique=True)
    op.create_table('shop_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('shop_name', sa.String(length=30), nullable=False),
    sa.Column('shop_introduction', sa.Text(), nullable=True),
    sa.Column('floor_send_cost', sa.Float(), nullable=True),
    sa.Column('send_cost', sa.Float(), nullable=True),
    sa.Column('notic', sa.String(length=200), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('shop_img_name', sa.String(length=50), nullable=True),
    sa.Column('box_price', sa.Float(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('province', sa.Integer(), nullable=False),
    sa.Column('city', sa.Integer(), nullable=False),
    sa.Column('area', sa.Integer(), nullable=False),
    sa.Column('detailed', sa.String(length=64), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lng', sa.Float(), nullable=False),
    sa.Column('contact', sa.PickleType(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user_shop.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('owner_id'),
    sa.UniqueConstraint('shop_name')
    )
    op.create_table('item_category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_name', sa.String(length=10), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('wx_order_no', sa.String(length=32), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('total_items', sa.Integer(), nullable=False),
    sa.Column('address_str', sa.String(length=200), nullable=False),
    sa.Column('receiver', sa.String(length=20), nullable=False),
    sa.Column('contact_phone', sa.String(length=11), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
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
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_num'),
    sa.UniqueConstraint('idcard_num'),
    sa.UniqueConstraint('service_num'),
    sa.UniqueConstraint('shop_id')
    )
    op.create_table('shop_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_name', sa.String(length=20), nullable=False),
    sa.Column('item_sales', sa.Integer(), nullable=False),
    sa.Column('item_stock', sa.Integer(), nullable=False),
    sa.Column('item_price', sa.Float(), nullable=False),
    sa.Column('item_introduction', sa.String(length=128), nullable=True),
    sa.Column('state', sa.Boolean(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('item_category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_category_id'], ['item_category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shop_id'], ['shop_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_specification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('specification_name', sa.String(length=15), nullable=False),
    sa.Column('additional_costs', sa.Float(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_num', sa.Integer(), nullable=False),
    sa.Column('item_price', sa.Float(), nullable=False),
    sa.Column('item_name', sa.String(length=20), nullable=False),
    sa.Column('specification_name', sa.String(length=15), nullable=True),
    sa.Column('additional_costs', sa.Float(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['shop_items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_personal.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_region_parent_id'), 'region', ['parent_id'], unique=False)
    op.create_index(op.f('ix_region_region_id'), 'region', ['region_id'], unique=False)
    op.create_index(op.f('ix_region_region_type'), 'region', ['region_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_region_region_type'), table_name='region')
    op.drop_index(op.f('ix_region_region_id'), table_name='region')
    op.drop_index(op.f('ix_region_parent_id'), table_name='region')
    op.drop_table('user_comment')
    op.drop_table('order_items')
    op.drop_table('item_specification')
    op.drop_table('shop_items')
    op.drop_table('shop_license')
    op.drop_table('orders')
    op.drop_table('item_category')
    op.drop_table('shop_info')
    op.drop_index(op.f('ix_admin_name'), table_name='admin')
    op.drop_table('admin')
    op.drop_table('address')
    op.drop_table('user_shop')
    op.drop_table('user_personal')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_index(op.f('ix_role_default'), table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###
