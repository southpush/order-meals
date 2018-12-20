# -*- coding: utf-8 -*-
import json

from flask_restful import Resource, reqparse

from app.api_1_0.response import general_response
from app.db.shop_db import get_delivery_shop
from app.db.user_db import add_in_db
from app.main.auth import login_required_personal


# 获取地理位置附近的商铺
from app.models import address
from app.models.order import orders, order_items
from app.models.shop import shop_items, item_specification, shop_info


class nearby_shop(Resource):
    def get(self, lat, lng):
        a = get_delivery_shop(lat=lat, lng=lng)
        info = []
        for i in a:
            info.append(i.get_simple_shop_info())
        return general_response(info={"shop_list": info})


class personal_orders(Resource):
    # 获取具体的某一条订单的
    @login_required_personal()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        id = data.parse_args()["order_id"]

        if not id:
            return general_response(err_code=101, status_code=400)

        order = user.order.filter_by(id=id).first()
        if order:
            info = order.get_order_dict_personal()
            return general_response(info=info)
        return general_response(err_code=408, status_code=404)

    # 下单
    @login_required_personal()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("item_list", type=str)
        data.add_argument("shop_id", type=int)
        data.add_argument("address_id", type=int)
        item_list = json.loads(data.parse_args()["item_list"])
        address_id = data.parse_args()["address_id"]
        shop_id = data.parse_args()["shop_id"]

        contact = user.address.filter_by(id=address_id).first()
        if not contact:
            return general_response(err_code=701, status_code=400)
        if not (shop_id and item_list):
            return general_response(err_code=101, status_code=400)
        shop = shop_info.query.filter_by(id=shop_id).first()
        if not shop:
            return general_response(err_code=407, status_code=404)
        order = orders(total_items=len(item_list), user_id=user.id, shop_id=shop_id,
                       address_str=contact.get_address_str(), contact_phone=contact.contact_phone,
                       receiver=contact.receiver, box_price=shop.box_price, send_cost=shop.send_cost)
        add_in_db(order)
        for a in item_list:
            item_id = a["item_id"]
            item_num = a["item_num"]
            item = shop_items.query.filter_by(shop_id=shop_id).filter_by(id=item_id).first()
            if not item:
                continue
            else:
                b = order_items(item_num=item_num, item_name=item.item_name, item_price=item.item_price,
                                order_id=order.id, item_id=item.id)
                try:
                    specification_id = a["specification_id"]
                except KeyError as e:
                    print(e.__repr__())
                    specification_id = None
                except TypeError as e:
                    print(e.__repr__())
                    specification_id = None
                print(specification_id)
                if specification_id:
                    specification = item_specification.query.filter_by(item_id=item.id).\
                        filter_by(id=specification_id).first()
                    if specification:
                        b.specification_name = specification.specification_name
                        b.additional_costs = specification.additional_costs
                add_in_db(b)
        num, price = order.count()
        return general_response(info={"item_num": num, "total_price": price})


class personal_orders_list(Resource):
    @login_required_personal()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("page", type=int)
        page = data.parse_args()["page"]
        pagination = user.order.order_by(orders.id.desc()).paginate(page, per_page=10, error_out=False)
        info = []
        for i in pagination.items:
            info.append(i.get_simple_dict_personal())
        return general_response(info={"orders": info})






