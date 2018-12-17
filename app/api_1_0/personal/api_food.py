# -*- coding: utf-8 -*-
import json

from flask_restful import Resource, reqparse

from app.api_1_0.response import general_response
from app.db.shop_db import get_delivery_shop
from app.db.user_db import add_in_db
from app.main.auth import login_required_personal


# 获取地理位置附近的商铺
from app.models.order import orders, order_items
from app.models.shop import shop_items


class nearby_shop(Resource):
    def get(self, lat, lng):
        a = get_delivery_shop(lat=lat, lng=lng)
        info = []
        for i in a:
            info.append(i.get_simple_shop_info())
        return general_response(info=info)


class personal_orders(Resource):
    # 获取具体的某一条订单的
    @login_required_personal()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        id = data.parse_args()["order_id"]
        order = user.order.filter_by(id=id).first()
        info = order.get_order_dict()
        return general_response(info=info)

    # 下单
    @login_required_personal()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("item_list", type=str)
        data.add_argument("shop_id", type=str)
        item_list = json.loads(data.parse_args()["item_list"])
        shop_id = data.parse_args()["shop_id"]
        order = orders(total_items=len(item_list), user_id=user.id, shop_id=shop_id)
        add_in_db(order)
        for a in item_list:
            item = shop_items.query.filter_by(shop_id=shop_id).filter_by(id=int(a["item_id"])).first()
            if item:
                a = order_items(item_num=int(a["item_num"]), item_name=item.item_name,
                                item_price=item.item_price, order_id=order.id, item_id=item.id)
                add_in_db(a)
        num, price = order.count()

        return general_response(info={"total_price": price, "total_num": num})


class personal_orders_list(Resource):
    @login_required_personal()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("page", type=int)
        page = data.parse_args()["page"]
        pagination = user.order.order_by(orders.id.desc()).paginate(page, per_page=10, error_out=False)
        info = []
        for i in pagination.items:
            info.append(i.get_simple_dict())
        return general_response(info={"orders": info})






