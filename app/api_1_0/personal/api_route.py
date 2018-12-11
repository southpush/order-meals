# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.personal import api_1_0_personal
from .api_user import user, getTest, getTest2, user_info
from app.api_1_0.errors import errors

api_personal = Api(api_1_0_personal, catch_all_404s=True, errors=errors)

# 注册路由
api_personal.add_resource(user, "/user")
api_personal.add_resource(user_info, "/user-info")
api_personal.add_resource(getTest, "/getTest")
api_personal.add_resource(getTest2, "/getTest2")


