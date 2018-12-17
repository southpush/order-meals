# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.shop import api_1_0_shop
from app.api_1_0.shop.api_orders import shop_order
from app.api_1_0.shop.api_shop import shop_info_application, working_shop_info, food_items
from .api_user import user, getTest2, user_info, testRL

api_shop = Api(api_1_0_shop)

# 注册路由

# 注册路由
api_shop.add_resource(user, '/user')
api_shop.add_resource(user_info, "/user-info")
api_shop.add_resource(shop_info_application, "/shop-info")
api_shop.add_resource(working_shop_info, "/working-shop-info")
api_shop.add_resource(getTest2, "/getTest2")
api_shop.add_resource(food_items, "/food_items")
api_shop.add_resource(shop_order, "/orders")

# 测试用的不需要code，自己设定openid登陆的路由
api_shop.add_resource(testRL, "/testRL")