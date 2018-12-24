# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.user import user_personal, user_shop


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


# 增加数据的通用方法
def add_in_db(what):
    try:
        db.session.add(what)
        db.session.commit()
        return what
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


# 更新数据通用方法
def update_in_db(what):
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


# 删除数据通用方法
def delete_in_db(what):
    try:
        db.session.delete(what)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


def add_in_db2(what):
    try:
        db.session.add(what)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        print(e.__repr__())
        return False