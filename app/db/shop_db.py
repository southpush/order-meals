# -*- coding: utf-8 -*-
from math import radians, cos, sin, asin, sqrt
from .. import db


# 计算两经纬度之间的距离的函数
from app.models.shop import shop_info


def haversine(lat1, lng1, lat2, lng2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


# 获取配送范围内的商家
def get_delivery_shop(lat, lng):
    lat = float(lat)
    lng = float(lng)
    rough_list = db.session.query(shop_info).\
        filter(shop_info.lat.between(lat - 0.02, lat + 0.02)).filter(shop_info.lng.between(lng - 0.02, lng + 0.02)).all()
    copy = rough_list[:]

    for a in range(len(rough_list)):
        if haversine(lat1=lat, lng1=lng, lat2=rough_list[a].lat, lng2=rough_list[a].lng) > 2000:
            copy.remove(rough_list[a])
    return copy






