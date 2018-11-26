# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.shop import api_1_0_shop

api_shop = Api(api_1_0_shop)

# 注册路由
