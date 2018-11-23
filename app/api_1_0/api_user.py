# -*- coding: utf-8 -*-
import json

from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify

import requests
from . import glovar


class getUser(Resource):
    def get(self):
        # addUser("naem11213")
        return jsonify({"data:": "hello !"})

    def post(self):
        # 获取post传来的数据，然后获取其中的json的规定的数据
        data = reqparse.RequestParser()
        data.add_argument("code", type=str)
        code = data.parse_args()["code"]

        whatget = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'
            % (glovar.AppID, glovar.AppSecret, code)
        )
        print(whatget.json())
        dict = whatget.json()
        print(dict["openid"])
        return jsonify({"data": "put"})






