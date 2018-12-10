"""change the way of head img save

Revision ID: bac709280da0
Revises: 2c7a504be470
Create Date: 2018-12-07 16:31:54.484301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bac709280da0'
down_revision = '2c7a504be470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('head_img',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.LargeBinary(length=2048), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('admin_ibfk_1', 'admin', type_='foreignkey')
    op.create_foreign_key(None, 'admin', 'role', ['role_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('order_items_ibfk_2', 'order_items', type_='foreignkey')
    op.drop_constraint('order_items_ibfk_1', 'order_items', type_='foreignkey')
    op.create_foreign_key(None, 'order_items', 'shop_items', ['item_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'order_items', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('orders_ibfk_2', 'orders', type_='foreignkey')
    op.drop_constraint('orders_ibfk_1', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'shop_info', ['shop_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'orders', 'user_personal', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('shop_info_ibfk_1', 'shop_info', type_='foreignkey')
    op.create_foreign_key(None, 'shop_info', 'user_shop', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('shop_items_ibfk_1', 'shop_items', type_='foreignkey')
    op.create_foreign_key(None, 'shop_items', 'shop_info', ['shop_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('shop_license_ibfk_1', 'shop_license', type_='foreignkey')
    op.create_foreign_key(None, 'shop_license', 'shop_info', ['shop_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('shopping_car_ibfk_1', 'shopping_car', type_='foreignkey')
    op.drop_constraint('shopping_car_ibfk_2', 'shopping_car', type_='foreignkey')
    op.create_foreign_key(None, 'shopping_car', 'user_personal', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'shopping_car', 'shop_items', ['item_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('user_address_ibfk_1', 'user_address', type_='foreignkey')
    op.create_foreign_key(None, 'user_address', 'user_personal', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('user_comment_ibfk_1', 'user_comment', type_='foreignkey')
    op.drop_constraint('user_comment_ibfk_3', 'user_comment', type_='foreignkey')
    op.drop_constraint('user_comment_ibfk_2', 'user_comment', type_='foreignkey')
    op.create_foreign_key(None, 'user_comment', 'user_personal', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_comment', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_comment', 'shop_items', ['item_id'], ['id'], ondelete='CASCADE')
    op.add_column('user_personal', sa.Column('head_img_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_personal', 'head_img', ['head_img_id'], ['id'])
    op.add_column('user_shop', sa.Column('head_img_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_shop', 'head_img', ['head_img_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_shop', type_='foreignkey')
    op.drop_column('user_shop', 'head_img_id')
    op.drop_constraint(None, 'user_personal', type_='foreignkey')
    op.drop_column('user_personal', 'head_img_id')
    op.drop_constraint(None, 'user_comment', type_='foreignkey')
    op.drop_constraint(None, 'user_comment', type_='foreignkey')
    op.drop_constraint(None, 'user_comment', type_='foreignkey')
    op.create_foreign_key('user_comment_ibfk_2', 'user_comment', 'orders', ['order_id'], ['id'])
    op.create_foreign_key('user_comment_ibfk_3', 'user_comment', 'user_personal', ['user_id'], ['id'])
    op.create_foreign_key('user_comment_ibfk_1', 'user_comment', 'shop_items', ['item_id'], ['id'])
    op.drop_constraint(None, 'user_address', type_='foreignkey')
    op.create_foreign_key('user_address_ibfk_1', 'user_address', 'user_personal', ['user_id'], ['id'])
    op.drop_constraint(None, 'shopping_car', type_='foreignkey')
    op.drop_constraint(None, 'shopping_car', type_='foreignkey')
    op.create_foreign_key('shopping_car_ibfk_2', 'shopping_car', 'user_personal', ['user_id'], ['id'])
    op.create_foreign_key('shopping_car_ibfk_1', 'shopping_car', 'shop_items', ['item_id'], ['id'])
    op.drop_constraint(None, 'shop_license', type_='foreignkey')
    op.create_foreign_key('shop_license_ibfk_1', 'shop_license', 'shop_info', ['shop_id'], ['id'])
    op.drop_constraint(None, 'shop_items', type_='foreignkey')
    op.create_foreign_key('shop_items_ibfk_1', 'shop_items', 'shop_info', ['shop_id'], ['id'])
    op.drop_constraint(None, 'shop_info', type_='foreignkey')
    op.create_foreign_key('shop_info_ibfk_1', 'shop_info', 'user_shop', ['owner_id'], ['id'])
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_ibfk_1', 'orders', 'shop_info', ['shop_id'], ['id'])
    op.create_foreign_key('orders_ibfk_2', 'orders', 'user_personal', ['user_id'], ['id'])
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.create_foreign_key('order_items_ibfk_1', 'order_items', 'shop_items', ['item_id'], ['id'])
    op.create_foreign_key('order_items_ibfk_2', 'order_items', 'orders', ['order_id'], ['id'])
    op.drop_constraint(None, 'admin', type_='foreignkey')
    op.create_foreign_key('admin_ibfk_1', 'admin', 'role', ['role_id'], ['id'])
    op.drop_table('head_img')
    # ### end Alembic commands ###
