# -*- coding: utf-8 -*-
import json

import requests
from flask import make_response

from app import glovar
from app.api_1_0.response import general_response
from app.db.user_db import add_in_db, update_in_db, delete_in_db
from app.main.auth import login_required_shop
from flask_restful import Resource, reqparse

from app.models.order import orders, order_status
from app.models.shop import shop_info, item_specification, item_category, shop_items


class shop_info_application(Resource):
    @login_required_shop()
    def get(self, user):
        if not user.shop:
            return general_response(err_code=303, status_code=404)
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
            return general_response()
        return general_response(err_code=602, status_code=400)

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
            return general_response()

        return general_response(err_code=601, status_code=400)


class shop_license_application(Resource):
    # 获取该商店的许可信息
    @login_required_shop()
    def get(self, user):
        if not user.shop:
            return general_response()
        pass

    @login_required_shop()
    def post(self, user):
        pass

    @login_required_shop()
    def put(self, user):
        pass

    @login_required_shop()
    def delete(self, user):
        pass


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
            return general_response(err_code=303, status_code=404)

        shop.floor_send_cost = floor_send_cost
        shop.send_cost = send_cost
        shop.notic = notic
        shop.box_price = box_price
        if update_in_db(shop):
            return general_response()
        return general_response(err_code=601, status_code=406)


class food_items(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument("shop_id", type=int)
        id = data.parse_args()["shop_id"]
        shop = shop_info.query.filter_by(id=id).first()
        if not shop:
            return general_response(err_code=407, status_code=404)
        category_list = shop.item_category.all()
        shop_items_list = shop.items.all()
        a_list = []
        for a in category_list:
            one_dict = {
                "category_id": a.id,
                "category_name": a.category_name,
            }
            a_list.append(one_dict)

        b_list = []
        for b in shop_items_list:
            b_list.append(b.get_item_detail())

        info = {
            "category_list": a_list,
            "shop_items_list": b_list,
            "shop_info": shop.get_shop_info()
        }

        return general_response(info=info)

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
        return general_response()


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
            return general_response()
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
                    return general_response()
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
                    return general_response()
                else:
                    return general_response(err_code=603, status_code=400)
        else:
            return general_response(err_code=405, status_code=404)


class received_orders(Resource):
    # 查看自己的可以接单的订单
    @login_required_shop()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("page", type=int)
        page = data.parse_args()["page"]
        order_list = user.shop.order.filter_by(status=order_status.waiting_for_receive).order_by(orders.id).\
            paginate(page, per_page=15, error_out=False)
        a = []
        for i in order_list.items:
            a.append(i.get_order_dict_shop())

        info = {
            "order_list": a,
            "has_next": order_list.has_next,
            "page_here": order_list.page,
            "per_page": order_list.per_page,
            "total_pages": order_list.pages,
            "total": order_list.total
        }
        return general_response(info=info)

    # 不接单
    @login_required_shop()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        order_id = data.parse_args()["order_id"]
        order = user.shop.order.filter_by(status=order_status.waiting_for_receive).filter_by(id=order_id).first()
        if order:
            order.status = order_status.shut_down_shop_no_receive
            update_in_db(order)
            return general_response()
        else:
            return general_response(err_code=408, status_code=404)

    # 接单
    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        order_id = data.parse_args()["order_id"]
        order = user.shop.order.filter_by(status=order_status.waiting_for_receive).filter_by(id=order_id).first()
        if order:
            order.status = order_status.waiting_for_delivery
            update_in_db(order)
            return general_response()
        else:
            return general_response(err_code=408, status_code=404)


class canceled_orders(Resource):
    # 获取用户摁了取消的需要商家处理的订单
    @login_required_shop()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("page", type=int)
        page = data.parse_args()["page"]
        pagination = user.shop.order.filter_by(status=order_status.personal_cancel).\
            order_by(orders.id.desc()).paginate(page, per_page=10, error_out=False)
        order_list = []
        for i in pagination.items:
            d = {}
            d.update(i.get_order_dict_shop())
            d.update(i.charge_back_info.get_charge_back_info_dict())
            order_list.append(d)
        info = {
            "order_list": order_list,
            "has_next": pagination.has_next,
            "page_here": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total": pagination.total
        }
        return general_response(info=info)

    # 拒绝取消订单
    @login_required_shop()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        data.add_argument("shop_reason", type=str)
        order_id = data.parse_args()["order_id"]
        shop_reason = data.parse_args()["shop_reason"]

        order = user.shop.order.filter_by(status=order_status.personal_cancel).filter_by(id=order_id).first()

        if order:
            if shop_reason:
                charge = order.charge_back_info
                charge.shop_reason = shop_reason
                order.status = order_status.shop_refuse
                update_in_db(order)
                update_in_db(charge)
            else:
                return general_response(err_code=101, status_code=400)
            return general_response()
        else:
            return general_response(err_code=408, status_code=404)

    # 接受取消订单的
    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("order_id", type=int)
        order_id = data.parse_args()["order_id"]

        order = user.shop.order.filter_by(status=order_status.personal_cancel).filter_by(id=order_id).first()

        if order:
            # 处理商家接受退款的
            order.status = order_status.shut_down_return_to_personal
            update_in_db(order)
            return general_response()
        else:
            return general_response(err_code=408, status_code=404)


