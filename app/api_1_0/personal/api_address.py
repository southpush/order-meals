# -*- coding: utf-8 -*-
import requests
from flask import make_response
from flask_restful import Resource, reqparse
from app import glovar
from app.api_1_0.response import general_response
from app.db.user_db import add_in_db, update_in_db, delete_in_db
from app.main.auth import login_required_personal
from app.models.address import address, Region


class receipted_address(Resource):
    # 这里的get只会返回权重最高的地址，即默认地址
    @login_required_personal()
    def get(self, user):
        a = user.address.order_by(address.weights.desc()).first()
        if a:
            info = {
                "address_str": a.get_address_str(),
                "address_dict": a.get_address_dict(),
                "lat": a.lat,
                "lng": a.lng,
                "contact_phone": a.contact_phone,
                "receiver": a.receiver,
                "address_id": a.id
            }
            return general_response(info=info)
        else:
            return general_response(err_code=403, status_code=404)

    @login_required_personal()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument('province_id', type=int)
        data.add_argument('city_id', type=int)
        data.add_argument('area_id', type=int)
        data.add_argument("detailed", type=str)
        data.add_argument("contact_phone", type=str)
        data.add_argument("receiver", type=str)

        province_id = data.parse_args()["province_id"]
        city_id = data.parse_args()["city_id"]
        area_id = data.parse_args()["area_id"]
        detailed = data.parse_args()["detailed"]
        contact_phone = data.parse_args()["contact_phone"]
        receiver = data.parse_args()["receiver"]

        if not (province_id and city_id and area_id and detailed and contact_phone and receiver):
            return general_response(err_code=101, status_code=400)

        a = address(province=province_id, city=city_id,
                    area=area_id, detailed=detailed, user_id=user.id,
                    receiver=receiver, contact_phone=contact_phone)

        if not (Region.query.filter_by(parent_id=1).filter_by(region_id=province_id).first()
                and Region.query.filter_by(parent_id=province_id).filter_by(region_id=city_id).first()
                and Region.query.filter_by(parent_id=city_id).filter_by(region_id=area_id).first()):
            return general_response(err_code=402, status_code=400)

        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        d = {
            "address": a.get_address_str(),
            "key": glovar.map_key
        }

        result = requests.get(url=url, params=d).json()
        a.lat = result["result"]["location"]["lat"]
        a.lng = result["result"]["location"]["lng"]

        if add_in_db(a):
            return general_response()
        return general_response(err_code=101, status_code=400)

    @login_required_personal()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument('province_id', type=int)
        data.add_argument('city_id', type=int)
        data.add_argument('area_id', type=int)
        data.add_argument("detailed", type=str)
        data.add_argument("contact_phone", type=str)
        data.add_argument("receiver", type=str)
        data.add_argument("address_id", type=int)

        province_id = data.parse_args()["province_id"]
        city_id = data.parse_args()["city_id"]
        area_id = data.parse_args()["area_id"]
        detailed = data.parse_args()["detailed"]
        contact_phone = data.parse_args()["contact_phone"]
        receiver = data.parse_args()["receiver"]
        address_id = data.parse_args()["address_id"]

        if not (province_id and city_id and area_id and detailed and contact_phone and receiver and address_id):
            return general_response(err_code=101, status_code=400)

        a = user.address.filter_by(id=address_id).first()
        if not a:
            return general_response(err_code=404, status_code=404)

        if not (Region.query.filter_by(parent_id=1).filter_by(region_id=province_id).first()
                and Region.query.filter_by(parent_id=province_id).filter_by(region_id=city_id).first()
                and Region.query.filter_by(parent_id=city_id).filter_by(region_id=area_id).first()):
            return general_response(err_code=402, status_code=400)

        if not (detailed and contact_phone and receiver):
            return general_response(err_code=101, status_code=400)

        a.contact_phone = contact_phone
        a.receiver = receiver
        a.province = province_id
        a.city = city_id
        a.area = area_id
        a.detailed = detailed

        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        d = {
            "address": a.get_address_str(),
            "key": glovar.map_key
        }

        result = requests.get(url=url, params=d).json()
        if result["status"] == 0:
            a.lat = result["result"]["location"]["lat"]
            a.lng = result["result"]["location"]["lng"]
        else:
            return general_response(info={"message": result["message"]}, status_code=400)

        if update_in_db(a):
            return general_response()
        return general_response(err_code=601, status_code=400)

    # 删除收货地址
    @login_required_personal()
    def delete(self, user):
        data = reqparse.RequestParser()
        data.add_argument('address_id', type=int)
        address_id = data.parse_args()['address_id']
        a = user.address.filter_by(id=address_id).first()
        if not a:
            return general_response(err_code=404, status_code=404)

        delete_in_db(a)

        return general_response()


class receipted_address_list(Resource):
    # 这个是返回收货地址的 list 的
    @login_required_personal()
    def get(self, user):
        address_list = user.address.order_by(address.weights.desc()).all()
        info = []
        if address_list:
            for a in address_list:
                info.append({
                    "address_str": a.get_address_str(),
                    "address_dict": a.get_address_dict(),
                    "lat": a.lat,
                    "lng": a.lng,
                    "contact_phone": a.contact_phone,
                    "receiver": a.receiver,
                    "address_id": a.id
                })
            return general_response(info=info)
        else:
            return general_response(err_code=403, status_code=404)

    # 设置默认地址（即更改地址的权重）
    @login_required_personal()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument('address_id', type=int)
        address_id = data.parse_args()['address_id']

        a = user.address.filter_by(id=address_id).first()
        b = user.address.order_by(address.weights.desc()).first()

        if not a:
            return general_response(err_code=404, status_code=404)
        a.weights = 100
        b.weights = 1

        update_in_db(a)
        update_in_db(b)

        return general_response()
