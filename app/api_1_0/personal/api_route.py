# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.personal import api_1_0_personal
from .api_user import user, getTest, getTest2, user_info, testRL, loginTest1
from .api_address import receipted_address, receipted_address_list
from .api_food import nearby_shop, personal_orders, personal_orders_list
from app.api_1_0.errors import errors

api_personal = Api(api_1_0_personal, catch_all_404s=True, errors=errors)

# 注册路由
api_personal.add_resource(user, "/user")
api_personal.add_resource(user_info, "/user-info")
api_personal.add_resource(receipted_address, "/receipted_address")
api_personal.add_resource(getTest, "/getTest")
api_personal.add_resource(getTest2, "/getTest2")
api_personal.add_resource(nearby_shop, "/nearby_shop/<lat>/<lng>")
api_personal.add_resource(personal_orders, "/orders")
api_personal.add_resource(personal_orders_list, "/orders_list")
api_personal.add_resource(receipted_address_list, "/receipted_address_list")

# 测试用的不需要code，自己设定openid登陆的路由
api_personal.add_resource(testRL, "/testRL")

