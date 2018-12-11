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

    rst.headers["Access-Control-Allow-Origin"] = "*"
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
        "message": "Fail in updating the shop info.",
        "code": 504
    },
    601: {
        "message": "Fail in updating in database.",
        "code": 601
    }
}
