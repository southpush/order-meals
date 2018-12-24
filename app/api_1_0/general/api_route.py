# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0.general import api_1_0_general
from app.api_1_0.errors import errors
from app.api_1_0.general.api_general import region, user_shop_head_image, user_personal_head_image, shop_image, \
    shop_item_image

api_general = Api(api_1_0_general, catch_all_404s=True, errors=errors)

# 注册路由
api_general.add_resource(region, "/region/<parent_id>")
api_general.add_resource(user_shop_head_image, "/shop_head", "/shop_head/<image_name>")
api_general.add_resource(user_personal_head_image, "/personal_head", "/personal_head/<image_name>")
api_general.add_resource(shop_image, "/shop_image", "/shop_image/<image_name>")
api_general.add_resource(shop_item_image, "/shop_item_image", "/shop_item_image/<image_name>")
