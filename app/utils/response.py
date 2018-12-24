# -*- coding: utf-8 -*-
from flask import make_response, jsonify


def general_response(info=None, err_code=None, status_code=200, token=None):
    if err_code:
        rst = make_response(jsonify(error_dict[err_code]), status_code)

    if info:
        rst = make_response(jsonify(info), status_code)
        if token:
            rst.set_cookie("token", token.decode("ascii"))

    if not err_code and not info and token:
        rst = make_response()
        rst.set_cookie("token", token.decode("ascii"))

    rst.headers["Access-Control-Allow-Origin"] = 'http://127.0.0.1:8020'
    rst.headers['Access-Control-Allow-Credentials'] = 'true'
    return rst


error_dict = {
    101: {
        "message": "Missing information.",
        "code": 101
    },
    102: {
        "message": "This wxUser has been registered.",
        "code": 102
    },
    103: {
        "message": "This phone has been registered.",
        "code": 103
    },
    104: {
        "message": "Add user error.",
        "code": 104
    },
    105: {
        "message": "Fail in uploading image into database.",
        "code": 105
    },
    106: {
        "message": "Can't find this picture.",
        'code': 106
    },
    107: {
        "message": "The file is too large to add in database, size limit in 1m.",
        "code": 107
    },
    201: {
        "message": "Invalid code.",
        "code": 201
    },
    202: {
        "message": "Can't find this user.",
        "code": 202
    },
    301: {
        "message": "Has no token.",
        "code": 301
    },
    302: {
        "message": "Fail in verify auth token.",
        "code": 302
    },
    401: {
        "message": "Can't find this picture.",
        "code": 401
    },
    501: {
        "message": "This shop user has owned a shop.",
        "code": 501
    },
    502: {
        "message": "Add shop error.",
        "code": 502
    },
    503: {
        'message': "This shop user has not shop.",
        "code": 503
    },
    504: {
        "message": "Fail in updating the shop info",
        "code": 504
    },
    1001: {
        "message": "手机号码/密码/角色不能为空",
        "code": 1001
    },
    1002: {
        "message": "手机号码格式不正确",
        "code": 1002
    },
    1003:{
        "message": "验证码不能为空",
        "code": 1003

    },
    1004: {
        "message": "验证码不正确",
        "code": 1004

    },
    1005: {
        "message": "密码不正确",
        "code": 1005

    },
    1006 : {
        "message": "该商家未申请商铺",
        "code": 1006
    },
    1007: {
        "message": "该商家未提交许可证",
        "code": 1007
    },
    1008: {
        "message": "无相关查询信息",
        "code": 1008
    },
    1009: {
        "message": "该用户还未曾下单",
        "code": 1009
    },
    403: {
        "message": "没有访问权限",
        "code": 403
    },




    2001: {
        "message": "出现异常",
        "code": 2001
    }

}
