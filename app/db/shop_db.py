# -*- coding: utf-8 -*-
from app import db


# 添加新的shop license
def add_license(license):
    try:
        db.session.add(license)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


# 添加新的shop
def add_shop(shop):
    try:
        db.session.add(shop)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return False


