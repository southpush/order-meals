# -*- coding: utf-8 -*-
from io import BytesIO

import requests
from flask_restful import Resource
from flask_restful import reqparse
from flask import make_response, json, request
from werkzeug.datastructures import FileStorage

from app.db.shop_db import get_delivery_shop
from app.db.user_db import update_in_db, delete_in_db

# from app.api_1_0.errors import APIException
from app.db.user_db import get_user_personal, add_in_db

from app.main.auth import get_openid, login_required_personal

# 用户进入小程序先登录，小程序传入code
from app.api_1_0.response import general_response
from app.models.user import user_personal


class user(Resource):
    # 用户登录
    def get(self):
        # 获取小程序传来的json，从中获取code
        data = reqparse.RequestParser()
        data.add_argument('code', type=str)

        code = data.parse_args()["code"]

        openid = get_openid(code)
        if not openid:
            return general_response(err_code=201, status_code=400)

        # 个人用户，如果已经验证过手机，就返回一个token
        # 否则返回错误代码，小程序跳转但验证手机页面
        user = get_user_personal(openid)
        if user:
            token = user.generate_auth_token()
            return general_response(token=token)
        else:
            return general_response(err_code=202, status_code=404)

    # 用户注册
    def post(self):
        data = reqparse.RequestParser()
        data.add_argument("code", type=str)
        data.add_argument("phone", type=str)
        data.add_argument("password", type=str)
        data.add_argument("nickname", type=str)
        data.add_argument("img_url", type=str)
        # data.add_argument("AppID", type=str)
        # data.add_argument("AppSecret", type=str)
        code = data.parse_args()["code"]
        phone = data.parse_args()["phone"]
        password = data.parse_args()["password"]
        nickname = data.parse_args()["nickname"]

        img_url = data.parse_args()["img_url"]
        if img_url:
            img = requests.get(img_url).content

        openid = get_openid(code)
        if not openid:
            return general_response(err_code=201, status_code=400)

        if not (code and phone and password and nickname and img):
            return general_response(err_code=101, status_code=400)
        elif get_user_personal(openid=openid):
            return general_response(err_code=102, status_code=403)
        elif get_user_personal(phone=phone):
            return general_response(err_code=103, status_code=403)
        else:
            user = user_personal(openid=openid, phone=phone, password=password, nickname=nickname)
            if add_in_db(user):
                storage = FileStorage(stream=BytesIO(img), content_type="image/jpeg")
                filename = str(user.id) + "default.jpg"
                storage.save("app/static/user_personal_head/" + filename)
                user.head_image_name = filename
                update_in_db(user)
                token = user.generate_auth_token()
                return general_response(token=token)
            else:
                return general_response(err_code=602, status_code=406)


# get方法为获取用户信息， post方法为获取表单，更改用户信息
class user_info(Resource):
    # 获取用户信息
    @login_required_personal()
    def get(self, user):
        return general_response(info=user.get_user_info(), status_code=200)

    # 修改用户信息
    @login_required_personal()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("nickname", type=str)
        nickname = data.parse_args()["nickname"]
        if not nickname:
            return general_response(err_code=101, status_code=400)
        user.nickname = nickname
        if not update_in_db(user):
            return general_response(err_code=601, status_code=400)
        return general_response()


class getTest(Resource):
    def get(self):
        return general_response(err_code=101, status_code=400)


class getTest2(Resource):
    @login_required_personal()
    def get(self, user):
        print(user)
        return True

    def post(self):
        data = reqparse.RequestParser()
        data.add_argument("file", type=str)
        file = request.files.get("file")
        if file:
            file.seek(0)
            return general_response()


class loginTest1(Resource):
    def get(self, lat, lng):
        a = get_delivery_shop(lat=lat, lng=lng)
        return general_response(info=a)


class testRL(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument('openid', type=str)
        openid = data.parse_args()["openid"]

        if not openid:
            return general_response(err_code=201, status_code=400)

        user = get_user_personal(openid)
        if user:
            token = user.generate_auth_token()
            return general_response(token=token)
        else:
            return general_response(err_code=202, status_code=404)

        # 用户注册
    def post(self):
        data = reqparse.RequestParser()
        data.add_argument("openid", type=str)
        data.add_argument("phone", type=str)
        data.add_argument("password", type=str)
        data.add_argument("nickname", type=str)
        openid = data.parse_args()["openid"]
        phone = data.parse_args()["phone"]
        password = data.parse_args()["password"]
        nickname = data.parse_args()["nickname"]

        if not openid:
            return general_response(err_code=201, status_code=400)
        elif get_user_personal(openid=openid):
            return general_response(err_code=102, status_code=403)
        elif get_user_personal(phone=phone):
            return general_response(err_code=103, status_code=403)
        else:
            user = user_personal(openid=openid, phone=phone, password=password, nickname=nickname)
            if add_in_db(user):
                token = user.generate_auth_token()
                return general_response(token=token)
            else:
                return general_response(err_code=602, status_code=406)
