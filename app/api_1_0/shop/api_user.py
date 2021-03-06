# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from io import BytesIO

import requests
from flask import make_response
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app.api_1_0.response import general_response
from app.db.user_db import get_user_shop, add_in_db, update_in_db

from app.main.auth import get_openid, login_required_shop

# 用户进入小程序先登录，小程序传入code
from app.models.user import user_shop


class user(Resource):
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
        user = get_user_shop(openid)
        if user:
            token = user.generate_auth_token()
            return general_response(token=token)
        else:
            return general_response(err_code=202, status_code=404)

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
        if img_url:
            img = requests.get(img_url).content

        openid = get_openid(code)
        if not openid:
            return general_response(err_code=201, status_code=400)

        if not (code and phone and password and nickname and img):
            return general_response(err_code=101, status_code=400)
        elif get_user_shop(openid=openid):
            return general_response(err_code=102, status_code=403)
        elif get_user_shop(phone=phone):
            return general_response(err_code=103, status_code=403)
        else:
            user = user_shop(openid=openid, phone=phone, password=password, nickname=nickname)
            if add_in_db(user):
                storage = FileStorage(stream=BytesIO(img), content_type="image/jpeg")
                filename = str(user.id) + user.nickname + ".jpg"
                storage.save("app/static/user_shop_head/" + filename)
                user.head_image_name = filename
                update_in_db(user)
                token = user.generate_auth_token()
                return general_response(token=token)
            else:
                return general_response(err_code=602, status_code=406)


class user_info(Resource):
    # 获取用户信息
    @login_required_shop()
    def get(self, user):
        return general_response(info=user.get_user_info(), status_code=200)

    @login_required_shop()
    def put(self, user):
        data = reqparse.RequestParser()
        data.add_argument("nickname", type=str)
        nickname = data.parse_args()["nickname"]
        if nickname:
            user.nickname = nickname
            if update_in_db(user):
                return general_response()
            else:
                return general_response(err_code=601, status_code=400)
        else:
            return general_response(err_code=101, status_code=400)


class getTest(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type=str, location="headers")
        login_key = parser.parse_args()["Authorization"]
        print(login_key)
        return True


class getTest2(Resource):
    @login_required_shop()
    def get(self, user):
        print(user)
        return True


class loginTest1(Resource):
    def get(self):
        pass


class testRL(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument('openid', type=str)
        openid = data.parse_args()["openid"]

        if not openid:
            return general_response(err_code=201, status_code=400)

        user = user_shop.query.filter_by(openid=openid).first()
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
        elif get_user_shop(openid=openid):
            return general_response(err_code=102, status_code=403)
        elif get_user_shop(phone=phone):
            return general_response(err_code=103, status_code=403)
        else:
            user = user_shop(openid=openid, phone=phone, password=password, nickname=nickname)
            if add_in_db(user):
                token = user.generate_auth_token()
                return general_response(token=token)
            else:
                return general_response(err_code=602, status_code=406)