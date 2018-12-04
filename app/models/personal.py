# -*- coding: utf-8 -*-
from .. import db


class user_address(db.Model):
    __tablename__ = "user_address"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    district = db.Column(db.String(20), nullable=True)
    detail = db.Column(db.String(128), nullable=True)
    receiver_phone = db.Column(db.String(11), nullable=True)
    receiver_name = db.Column(db.String(20), nullable=True)
    geocoding = db.Column(db.String(40), nullable=True)

    # 外鍵
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id"), nullable=False)

    def __repr__(self):
        return "<%r's address, id=%r>" % (self.user.nickname, self.id)


class comment(db.Model):
    __tablename__ = "user_comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)

    # 外鍵
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id"), nullable=False)

    def __repr__(self):
        return "<comment id = %r>" % self.id


class shopping_car(db.Model):
    __tablename__ = "shopping_car"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_num = db.Column(db.Integer, nullable=False)

    # 外鍵
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id"), nullable=False)

    def __repr__(self):
        return "<shopping car for %r , shopping car id '%r'>" % (self.user.nicknamem, self.id)
