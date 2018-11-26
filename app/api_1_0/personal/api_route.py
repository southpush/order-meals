# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.personal import api_1_0_personal
from .api_user import userLogin, getTest, getTest2, Register_personal
from app.api_1_0.errors import errors

api_personal = Api(api_1_0_personal, catch_all_404s=True, errors=errors)

# 注册路由
api_personal.add_resource(userLogin, '/getuser')
api_personal.add_resource(getTest, "/getTest")
api_personal.add_resource(getTest2, "/getTest2")
api_personal.add_resource(Register_personal, "/register-personal")
