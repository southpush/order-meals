# -*- coding: utf-8 -*-
import datetime
from app import db
import hashlib
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from .role import Permission
from .role import Role
from .. import loginmanager

from flask import json





# MD5加密：
def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class Admin( UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    admin_slat = db.Column(db.String(64))
    admin_phone = db.Column(db.String(11), unique=True)
    c_time = db.Column(db.DateTime, default=datetime.datetime.now)
    head_img = db.Column(db.LargeBinary(length=2048), nullable=True)

    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # 反向引用
    # user_personal = db.relationship('user_user_personal', backref='admin')
    # user_shop = db.relationship('user_user_shop', backref='admin')
    # orders = db.relationship('order_orders', backref='admin')

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        # if self.role is None:
        #     if self.role is None:
        #         self.role = Role.query.filter_by(default=True).first()


    def can(self, permissions):
        return self.role is not None and (self.role.permission & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # 将adminpass设置成不可读属性
    @property
    def adminpass(self):
        raise AttributeError('password is not a readable attribute')

    # 将adminpass设置成只可写属性，参数传入adminpass，然后将adminpass的slat值存起来
    @adminpass.setter
    def adminpass(self, adminpass):
        self.admin_slat = get_md5(adminpass)

    # admin的adminpass验证传入adminpass，进行验证
    def verify_adminpass(self, adminpass):
        if get_md5(adminpass) == self.admin_slat:
            return True
        else:
            return False

    def __repr__(self):
        return '<Admin %s>' % self.name


class AnonymousAdmin(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False

def ctd(obj):
    # result = json.dumps(obj, default=lambda obj: obj.__dict__)
    # return result
    role = Role.query.filter_by(id=obj.role_id).first()
    return {
        'name' : obj.name,
        'id' :obj.id,
        'phone' : obj.admin_phone,
        'role':role.name
    }

login_manager.LoginManager.anonymous_user = AnonymousAdmin




