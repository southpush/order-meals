# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.general import api_1_0_general
from app.api_1_0.errors import errors
from app.api_1_0.general.api_general import img

api_general = Api(api_1_0_general, catch_all_404s=True, errors=errors)

# 注册路由
api_general.add_resource(img, "/img")

