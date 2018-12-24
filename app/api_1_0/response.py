# -*- coding: utf-8 -*-
from flask import make_response, jsonify


def general_response(info=None, err_code=None, status_code=200, token=None):
    if err_code:
        rst = make_response(jsonify(error_dict[err_code]), status_code)

    if info:
        c = {"code:": 0, "message": "Success."}
        c.update(info)
        rst = make_response(jsonify(c), status_code)
        if token:
            rst.set_cookie("token", token.decode("ascii"))

    if not err_code and not info and token:
        rst = make_response(jsonify({"code:": 0, "message": "Success."}))
        rst.set_cookie("token", token.decode("ascii"))

    if not info and not err_code and not token:
        rst = make_response(jsonify({"code:": 0, "message": "Success."}), 200)

    rst.headers["Access-Control-Allow-Origin"] = "*"
    return rst


error_dict = {
    101: {
        "message": "传入的数据缺少某个字段。",
        "code": 101
    },
    102: {
        "message": "该微信用户已被注册过。",
        "code": 102
    },
    103: {
        "message": "这个电话已经注册过。",
        "code": 103
    },
    107: {
        "message": "传入文件过大，请限制在1m之内。.",
        "code": 107
    },
    108: {
        "message": "传入文件格式不正确，请确认图片格式为jpg、jpeg或png。",
        "code": 108
    },
    201: {
        "message": "无效的微信code。",
        "code": 201
    },
    202: {
        "message": "无法找到该用户。",
        "code": 202
    },
    301: {
        "message": "缺少登陆令牌。",
        "code": 301
    },
    302: {
        "message": "验证登陆令牌失败。",
        "code": 302
    },
    303: {
        "message": "该用户尚未注册商铺。",
        "code": 303
    },
    402: {
        "message": "错误的省市区关系或错误的地理编码",
        "code": 402
    },
    403: {
        "message": "该用户尚未添加地址。",
        "code": 403
    },
    404: {
        "message": '无法找到该地址。',
        "code": 404
    },
    405: {
        "message": "无法找到该商品规格",
        "code": 405
    },
    406: {
        "message": "无法在该商店找到该商品。",
        "code": 406
    },
    407: {
        "message": "无法找到该商铺。",
        "code": 407
    },
    408: {
        "message": "无法找到该订单。",
        "code": 408
    },
    409: {
        "message": "无法找到该图片。",
        "code": 409
    },
    410: {
        "message": "无法找到该地区。",
        "code": 410
    },
    411: {
        "message": "无法找到该收藏。",
        "code": 411
    },
    501: {
        "message": "该商铺用户已经注册过一个商铺。",
        "code": 501
    },
    601: {
        "message": "数据库更新数据时出现不可预测的错误。",
        "code": 601
    },
    602: {
        "message": "数据库添加数据时出现不可预测的错误。",
        "code": 602
    },
    603: {
        "message": "数据库删除数据时出现不可预测的错误。",
        "code": 603
    },
    701: {
        "message": "Incorrect receiver information.",
        "code": 701
    },
    702: {
        "message": "错误的收货信息，无法找到该收货信息。",
        "code": 702
    },
    703: {
        "message": "该订单所处的状态无法取消订单。",
        "code": 703
    },
    704: {
        "message": "该订单已超过支付时间。",
        "code": 704
    }
}
