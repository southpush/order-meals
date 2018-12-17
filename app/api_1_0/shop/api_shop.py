# -*- coding: utf-8 -*-
import json

import requests
from flask import make_response

from app import glovar
from app.api_1_0.response import general_response
from app.db.user_db import add_in_db, update_in_db
from app.main.auth import login_required_shop
from flask_restful import Resource, reqparse
from app.models.shop import shop_info, item_specification, item_category, shop_items


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
        data.add_argument("shop_introduction", type=str)

        # 改过的这些字段
        data.add_argument('province_id', type=int)
        data.add_argument('city_id', type=int)
        data.add_argument('area_id', type=int)
        data.add_argument("detailed", type=str)
        data.add_argument("contact", type=str)

        province_id = data.parse_args()["province_id"]
        city_id = data.parse_args()["city_id"]
        area_id = data.parse_args()["area_id"]
        detailed = data.parse_args()["detailed"]
        shop_name = data.parse_args()["shop_name"]
        shop_introduction = data.parse_args()["shop_introduction"]
        contact = data.parse_args()["contact"]
        contact = json.loads(contact)

        if not (shop_name and shop_introduction and detailed and province_id and city_id
                and area_id and contact):
            return general_response(err_code=101, status_code=400)

        info = shop_info(shop_name=shop_name, contact=contact, owner_id=user.id, shop_introduction=shop_introduction,
                         province=province_id, city=city_id, area=area_id, detailed=detailed)

        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        d = {
            "address": info.get_address_str(),
            "key": glovar.map_key
        }
        result = requests.get(url=url, params=d).json()
        info.lat = result["result"]["location"]["lat"]
        info.lng = result["result"]["location"]["lng"]

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


class food_items(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument("shop_id", type=int)
        id = data.parse_args()["shop_id"]
        shop = shop_info.query.filter_by(id=id).first()
        category_list = shop.item_category.all()
        info = []
        for a in category_list:
            one_dict = {
                "category_id": a.id,
                "category_name": a.category_name
            }
            item_list = []
            for b in a.items.all():
                item_list.append(b.get_item_detail())
            one_dict["item_list"] = item_list
            info.append(one_dict)

        return general_response(info={"food": info})

    @login_required_shop()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("item_list", type=str)
        item_list = json.loads(data.parse_args()["item_list"])
        for item in item_list:
            category = item_category.query.filter(item_category.shop_id == user.shop.id).\
                filter_by(category_name=item["category"]).first()
            # 要判断有没有这个类别，没有就要新建一个
            if not category:
                category = item_category(category_name=item['category'], shop_id=user.shop.id)
                add_in_db(category)
            new_item = shop_items(item_name=item["item_info"]["item_name"],
                                  item_price=float(item["item_info"]["item_price"]),
                                  item_introduction=item["item_info"]["item_introduction"],
                                  shop_id=user.shop.id, item_category_id=category.id)
            add_in_db(new_item)
        return make_response()






