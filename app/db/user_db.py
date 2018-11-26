# -*- coding: utf-8 -*-
from .. import db
from ..models.user import user_personal, user_shop
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError


# 查询用户,根据传入参数来判断是用openid来登陆还是手机号登陆
# 用来判断用户是否存在
def get_user_personal(openid=None, phone=None):
    if openid:
        user = user_personal.query.filter_by(openid=openid).first()
        return user if user else False
    else:
        if not phone:
            return False
        else:
            user = user_personal.query.filter_by(phone=phone).first()
            return user if user else False


# 查询商铺用户的
def get_user_shop(openid=None, phone=None):
    if openid:
        user = user_shop.query.filter_by(openid=openid).first()
        return user if user else False
    else:
        if not phone:
            return False
        else:
            user = user_shop.query.filter_by(phone=phone).first()
            return user if user else False


# 添加新用户
def add_user_personal(user):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


