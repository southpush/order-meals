# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.shop import api_1_0_shop
from app.api_1_0.shop.api_shop import shop_info_application, working_shop_info
from .api_user import user, getTest2, user_info

api_shop = Api(api_1_0_shop)

# 注册路由

# 注册路由
api_shop.add_resource(user, '/user')
api_shop.add_resource(user_info, "/user-info")
api_shop.add_resource(shop_info_application, "/shop-info")
api_shop.add_resource(working_shop_info, "/working-shop-info")
api_shop.add_resource(getTest2, "/getTest2")
