# -*- coding: utf-8 -*-
import requests
from flask import request

from app.glovar import AppID, AppSecret
from app.api_1_0.response import general_response
from app.models.user import user_personal, user_shop


# 个人用户登录装饰器
def login_required_personal():
    def decorator(func):
        def wrapper(*args, **kw):
            token = request.cookies.get("token")
            if not token:
                return general_response(err_code=301, status_code=401)
            user = user_personal.verify_auth_token(token)
            if user:
                return func(self=func, user=user)
            else:
                return general_response(err_code=302, status_code=401)
        return wrapper
    return decorator


# 商铺用户登陆装饰器
def login_required_shop():
    def decorator(func):
        def wrapper(*args, **kw):
            token = request.cookies.get("token")
            if not token:
                return general_response(err_code=301, status_code=401)
            user = user_shop.verify_auth_token(token)
            if user:
                return func(self=func, user=user)
            else:
                return general_response(err_code=302, status_code=401)
        return wrapper
    return decorator


def get_openid(code):
    try:
        get_from_wx = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'
            % (AppID, AppSecret, code)
        ).json()
        return get_from_wx["openid"]
    except Exception as e:
        print(repr(e))
        return False



