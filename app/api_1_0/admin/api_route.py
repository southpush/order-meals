# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.admin import api_1_0_admin

api_admin = Api(api_1_0_admin)

# 注册路由
