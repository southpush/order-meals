# -*- coding: utf-8 -*-
import requests
from flask_restful import reqparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.glovar import secret_key, AppID, AppSecret
from app.models.user import user_personal


def login_required_personal():
    def decorator(func):
        def wrapper(*args, **kw):
            parser = reqparse.RequestParser()
            parser.add_argument("Authorization", type=str)
            token = parser.parse_args()["Authorization"]
            if not token:
                return {"errMsg": "Has no token"}, 404
            user = user_personal.verify_auth_token(token)
            if user:
                return func(self=func, user=user)
            else:
                return {"errMsg": "Fail in verify auth token"}, 404
        return wrapper
    return decorator


def login_required_shop():
    def decorator(func):
        def wrapper(*args, **kw):
            parser = reqparse.RequestParser()
            parser.add_argument("Authorization", type=str)
            token = parser.parse_args()["Authorization"]
            if not token:
                return {"errMsg": "Has no token"}, 404
            user = user_personal.verify_auth_token(token)
            if user:
                return func(self=func, user=user)
            else:
                return {"errMsg": "Fail in verify auth token"}, 404
        return wrapper
    return decorator


def getToken_personal(id):
    s = Serializer(secret_key, expires_in=7200)
    return s.dumps({"id": id})


def getOpenid(code):
    try:
        getFromWx = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'
            % (AppID, AppSecret, code)
        ).json()
        return getFromWx["openid"]
    except Exception as e:
        print(repr(e))
        return False


