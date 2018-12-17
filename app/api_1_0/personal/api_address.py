# -*- coding: utf-8 -*-
import requests
from flask import make_response
from flask_restful import Resource, reqparse
from app import glovar
from app.api_1_0.response import general_response
from app.db.user_db import add_in_db
from app.main.auth import login_required_personal
from app.models.address import address


class receipted_address(Resource):
    @login_required_personal()
    def get(self, user):
        info = {
            "address_str": user.address.get_address_str,
            "address_dict": user.address.get_address_dict(),
            "lat": user.address.lat,
            "lng": user.address.lng
        }
        return general_response(info=info)

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

        a = address(province=province_id, city=city_id,
                    area=area_id, detailed=detailed, user_id=user.id,
                    receiver=receiver, contact_phone=contact_phone)

        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        d = {
            "address": a.get_address_str(),
            "key": glovar.map_key
        }
        result = requests.get(url=url, params=d).json()
        a.lat = result["result"]["location"]["lat"]
        a.lng = result["result"]["location"]["lng"]

        if add_in_db(a):
            return make_response()
        return general_response(err_code=101, status_code=400)


def haversine(address1, address2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [address1.lng, address1.lat, address2.lng, address2.lat])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000
