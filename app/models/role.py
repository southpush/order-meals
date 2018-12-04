#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 14:55
# @Author  : Min
# @Version : 1.0
from .. import db


# 角色表
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    default = db.Column(db.Boolean,default= False, index=True)
    permission = db.Column(db.Integer)

    # 反向引用
    admin = db.relationship('admin', backref='role')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            "USER": (Permission.FOLLOW, True),
            "SHOPADMIN": (Permission.SHOPERADMIN, False),
            "USERADMIN": (Permission.USERADMIN, False),
            "ADMIN": (0x80, False)

        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>'% self.name


# 辅助类 角色权限
class Permission:
    FOLLOW = 0x01  # 用户
    SHOPERADMIN = 0x02  # 商铺管理员
    USERADMIN = 0x04  # 用户管理员
    ADMINISTER = 0x00 #超级管理员权限