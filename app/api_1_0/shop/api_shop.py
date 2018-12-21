# -*- coding: utf-8 -*-
import json

import requests
from flask import make_response

from app import glovar
from app.api_1_0.response import general_response
from app.db.user_db import add_in_db, update_in_db, delete_in_db
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
        shop = user.shop

        if not shop:
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
        shop.shop_name = shop_name
        shop.contact = contact
        shop.shop_introduction = shop_introduction
        shop.province = province_id
        shop.city = city_id
        shop.area = area_id
        shop.detailed = detailed

        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        d = {
            "address": info.get_address_str(),
            "key": glovar.map_key
        }
        result = requests.get(url=url, params=d).json()
        shop.lat = result["result"]["location"]["lat"]
        shop.lng = result["result"]["location"]["lng"]

        if update_in_db(info):
            return make_response("", 204)

        return general_response(err_code=601, status_code=400)


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
            return make_response("", 204)
        return general_response(err_code=504, status_code=406)


class food_items(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument("shop_id", type=int)
        id = data.parse_args()["shop_id"]
        shop = shop_info.query.filter_by(id=id).first()
        if not shop:
            return general_response(err_code=407, status_code=404)
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
        return make_response("", 204)


# 食品规格的
class food_specification(Resource):
    # 获取该食品的规格
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument("item_id", type=str)
        item_id = data.parse_args()["item_id"]

        item = shop_items.query.filter_by(id=item_id).first()
        specification_list = item.specification.all()
        info = []
        for i in specification_list:
            info.append(i.get_specification_dict())

        return general_response(info={"specification_list": info})

    # 商家上传规格数据
    @login_required_shop()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("specification_name", type=str)
        data.add_argument("additional_costs", type=float)
        data.add_argument("item_id", type=int)
        specification_name = data.parse_args()["specification_name"]
        additional_costs = data.parse_args()["additional_costs"]
        item_id = data.parse_args()["item_id"]

        if not user.shop.items.filter_by(id=item_id).all():
            return general_response(err_code=406, status_code=404)

        a = item_specification(specification_name=specification_name, additional_costs=additional_costs,
                               item_id=item_id)

        if add_in_db(a):
            return make_response("", 204)
        return general_response(err_code=602, status_code=400)

    # 商家修改规格参数
    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("specification_name", type=str)
        data.add_argument("additional_costs", type=float)
        data.add_argument("specification_id", type=int)
        specification_name = data.parse_args()["specification_name"]
        additional_costs = data.parse_args()["additional_costs"]
        specification_id = data.parse_args()["specification_id"]

        a = item_specification.query.filter_by(id=specification_id).first()

        if a:
            if a.item in user.shop.items.all():
                a.specification_name = specification_name
                a.additional_costs = additional_costs
                if update_in_db(a):
                    return make_response("", 204)
                return general_response(err_code=601, status_code=400)
        return general_response(err_code=405, status_code=404)

    # 商家删除规格
    @login_required_shop()
    def delete(self, user):
        data = reqparse.RequestParser()
        data.add_argument("specification_id", type=int)
        specification_id = data.parse_args()["specification_id"]

        a = item_specification.query.filter_by(id=specification_id).first()

        if a:
            if a.item in user.shop.items.all():
                if delete_in_db(a):
                    return make_response("", 204)
                else:
                    return general_response(err_code=603, status_code=400)
        else:
            return general_response(err_code=405, status_code=404)

