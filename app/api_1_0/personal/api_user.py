# -*- coding: utf-8 -*-
import requests
from flask_restful import Resource
from flask_restful import reqparse
from flask import make_response

# from app.api_1_0.errors import APIException
from app.db.user_db import get_user_personal, add_in_db

from app.main.auth import get_openid, login_required_personal

# 用户进入小程序先登录，小程序传入code
from app.api_1_0.response import general_response
from app.models.user import user_personal, head_img


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
        code = data.parse_args()["code"]
        phone = data.parse_args()["phone"]
        password = data.parse_args()["password"]
        nickname = data.parse_args()["nickname"]

        img_url = data.parse_args()["img_url"]
        if img_url:
            img = requests.get(img_url).content
            img_obj = add_in_db(head_img(img=img))
            img_id = img_obj.id

        openid = get_openid(code)
        if not openid:
            return general_response(err_code=201, status_code=400)

        if not (code and phone and password and nickname and img_id):
            return general_response(err_code=101, status_code=400)
        elif get_user_personal(openid=openid):
            return general_response(err_code=102, status_code=403)
        elif get_user_personal(phone=phone):
            return general_response(err_code=103, status_code=403)
        else:
            user = user_personal(openid=openid, phone=phone, password=password, head_img_id=img_id,
                                 nickname=nickname)
            if add_in_db(user):
                token = user.generate_auth_token()
                return general_response(token=token)
            else:
                return general_response(err_code=104, status_code=406)


# get方法为获取用户信息， post方法为获取表单，更改用户信息
class user_info(Resource):
    # 获取用户信息
    @login_required_personal()
    def get(self, user):
        return general_response(info=user.get_user_info(), status_code=200)


class getTest(Resource):
    def get(self):
        return general_response(err_code=101, status_code=201)


class getTest2(Resource):
    @login_required_personal()
    def get(self, user):
        print(user)
        return True


class loginTest1(Resource):
    def get(self):
        rst = make_response("sdf", None)
        return rst


