# -*- coding: utf-8 -*-
import requests
from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify

# from app.api_1_0.errors import APIException
from app.db.user_db import get_user_personal, add_user_personal

from app.main.auth import getToken_personal, getOpenid, login_required_personal

# 用户进入小程序先登录，小程序传入code
from app.models.user import user_personal


class userLogin(Resource):
    def get(self):
        # 获取小程序传来的json，从中获取code
        data = reqparse.RequestParser()
        data.add_argument('code', type=str)

        code = data.parse_args()["code"]

        openid = getOpenid(code)

        # 个人用户，如果已经验证过手机，就返回一个token
        # 否则返回错误代码，小程序跳转但验证手机页面
        user = get_user_personal(openid)
        token = user.generate_auth_token()
        if user:
            return jsonify({"token": token.decode("ascii"), "id": user.id})
        else:
            return {"errMsg": "Can't find this user"}, 404


# 注册用户
class Register_personal(Resource):
    def post(self):
        data = reqparse.RequestParser()
        data.add_argument("code", type=str)
        data.add_argument("phone", type=str)
        data.add_argument("password", type=str)
        data.add_argument("nickname", type=str)
        data.add_argument("img_url", type=str)
        code = data.parse_args()["code"]
        phone = data.parse_args()["phone"]
        password = data.parse_args()["password"]
        nickname = data.parse_args()["nickname"]
        img_url = data.parse_args()["img_url"]
        img = requests.get(img_url).content

        openid = getOpenid(code)

        print("phone = " + phone)
        print("password = " + password)
        print("code = " + code)
        print("openid = " + openid)
        print("nickname = " + nickname)
        print(img)

        # 设一个状态，1代表缺失code或phone
        # 2代表openid已被注册
        # 3代表phone已被注册
        # 4加入失败
        if not (code and phone):
            return {"errMsg": "without code or phone", "errCode": 1}, 400
        elif get_user_personal(openid=openid):
            return {"errMsg": "This wxUser has been registered", "errCode": 2}, 400
        elif get_user_personal(phone=phone):
            return {"errMsg": "This phone has been registered", "errCode": 3}, 400
        else:
            user = user_personal(openid=openid, phone=phone, password=password, head_img=img,
                                 nickname=nickname)
            if add_user_personal(user):
                token = user.generate_auth_token()
                return jsonify({"token": token.decode("ascii")})
            else:
                return {"errMsg": 'add user error', "errCode": 4}, 400


class getTest(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type=str, location="headers")
        login_key = parser.parse_args()["Authorization"]
        print(login_key)
        return True


class getTest2(Resource):
    @login_required_personal()
    def get(self, user):
        print(user)
        return True


class loginTest1(Resource):
    def get(self):
        pass


