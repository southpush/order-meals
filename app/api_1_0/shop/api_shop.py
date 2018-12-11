# -*- coding: utf-8 -*-
from flask import make_response

from app.api_1_0.response import general_response
from app.db.user_db import add_in_db, update_in_db
from app.main.auth import login_required_shop
from flask_restful import Resource, reqparse


# 用于注册商铺
from app.models.shop import shop_info


class shop_info_application(Resource):
    @login_required_shop()
    def get(self, user):
        if not user.shop:
            return general_response(err_code=503, status_code=404)
        shop_dict = user.shop.get_shop_info()
        return general_response(shop_dict)

    @login_required_shop()
    def post(self, user):
        # 如果无法获取到该用户的shop再给申请
        if user.shop:
            return general_response(err_code=501, status_code=400)

        data = reqparse.RequestParser()
        data.add_argument("shop_name", type=str)
        data.add_argument("contact_name", type=str)
        data.add_argument("contact_phone", type=str)
        data.add_argument("geocoding", type=str)
        data.add_argument("address", type=str)
        data.add_argument("shop_introduction", type=str)

        shop_name = data.parse_args()["shop_name"]
        contact_name = data.parse_args()["contact_name"]
        contact_phone = data.parse_args()["contact_phone"]
        geocoding = data.parse_args()["geocoding"]
        address = data.parse_args()["address"]
        shop_introduction = data.parse_args()["shop_introduction"]

        if not (shop_name and contact_phone and contact_name and geocoding and address
        and shop_introduction):
            return general_response(err_code=101, status_code=400)

        info = shop_info(shop_name=shop_name, contact_name=contact_name, contact_phone=contact_phone,
                         geocoding=geocoding, address=address, owner_id=user.id, shop_introduction=shop_introduction)

        if add_in_db(info):
            return make_response()

        return general_response(err_code=502, status_code=400)

    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("shop_name", type=str)
        data.add_argument("contact_name", type=str)
        data.add_argument("contact_phone", type=str)
        data.add_argument("geocoding", type=str)
        data.add_argument("address", type=str)
        data.add_argument("shop_introduction", type=str)

        shop_name = data.parse_args()["shop_name"]
        contact_name = data.parse_args()["contact_name"]
        contact_phone = data.parse_args()["contact_phone"]
        geocoding = data.parse_args()["geocoding"]
        address = data.parse_args()["address"]
        shop_introduction = data.parse_args()["shop_introduction"]

        if not (shop_name and contact_phone and contact_name and geocoding and address
                and shop_introduction):
            return general_response(err_code=101, status_code=400)
        shop = user.shop
        shop.shop_name = shop_name
        shop.contact_name = contact_name
        shop.contact_phone = contact_phone
        shop.geocoding = geocoding
        shop.address = address
        shop.shop_introduction = shop_introduction
        if update_in_db(shop):
            return make_response()
        else:
            return general_response(err_code=504, status_code=406)


class working_shop_info(Resource):
    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("floor_send_cost", type=float)
        data.add_argument("send_cost", type=float)
        data.add_argument("notic", type=str)
        data.add_argument("box_price", type=float)

        floor_send_cost = data.parse_args()["floor_send_cost"]
        send_cost = data.parse_args()["send_cost"]
        notic = data.parse_args()["notic"]
        box_price = data.parse_args()["box_price"]
        shop = user.shop
        if not shop:
            return general_response(err_code=503, status_code=404)

        shop.floor_send_cost = floor_send_cost
        shop.send_cost = send_cost
        shop.notic = notic
        shop.box_price = box_price
        if update_in_db(shop):
            return make_response()
        return general_response(err_code=504, status_code=406)






