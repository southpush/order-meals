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
        "message": "The file is too large, size limit in 1m.",
        "code": 107
    },
    108: {
        "message": "The file format is incorrect.",
        "code": 108
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
    303: {
        "message": "This user has not shop.",
        "code": 303
    },
    401: {
        "message": "Can't find this picture.",
        "code": 401
    },
    402: {
        "message": "Incorrect relationship or incorrect region id.",
        "code": 402
    },
    403: {
        "message": "This user has not address.",
        "code": 403
    },
    404: {
        "message": 'No such address.',
        "code": 404
    },
    405: {
        "message": "No such item specification.",
        "code": 405
    },
    406: {
        "message": "This shop has no such shop item.",
        "code": 406
    },
    407: {
        "message": "No such shop.",
        "code": 407
    },
    408: {
        "message": "No such order.",
        "code": 408
    },
    409: {
        "message": "No such image.",
        "code": 409
    },
    410: {
        "message": "No such region.",
        "code": 410
    },
    411: {
        "message": "No such favorites.",
        "code": 411
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
    },
    602: {
        "message": "Fail in adding in database.",
        "code": 602
    },
    603: {
        "message": "Fail in delete in database.",
        "code": 603
    },
    701: {
        "message": "Incorrect receiver information.",
        "code": 701
    },
    702: {
        "message": "Incorrect file name.",
        "code": 702
    },
    703: {
        "message": "This order status can't be canceled",
        "code": 703
    },
    704: {
        "message": "This order has over the payment time.",
        "code": 704
    }
}
