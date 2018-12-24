#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 16:44
# @Author  : Min
# @Version : 1.0
# 添加新用户
from .. import db
from app.models.admin import Admin


def add_admin(admin):
    try:
        db.session.add(admin)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


def query_admin(admin):
    try:
        db.session.query(admin)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


def edit_admin(admin):
    try:
        db.session.edit(admin)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


# 获取图片的
def get_img(img_id=None):
    if img_id:
        img = Admin.head_img.query.filter_by(id=img_id).first()
        return img.img if img else False
    return False
