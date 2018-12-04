# -*- coding: utf-8 -*-
from datetime import datetime

from .. import db


class shop_info(db.Model):
    __tablename__ = "shop_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(30), nullable=False, unique=True)
    shop_introduction = db.Column(db.Text, nullable=True)
    contact_name = db.Column(db.String(30), nullable=False)
    contact_phone = db.Column(db.String(11), nullable=False, unique=True)
    geocoding = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    floor_send_cost = db.Column(db.Float, nullable=True, default=0)
    send_cost = db.Column(db.Float, nullable=True, default=0)
    notic = db.Column(db.String(200), nullable=True)
    score = db.Column(db.Float, nullable=True, default=0)
    shop_img = db.Column(db.LargeBinary, nullable=True)
    box_price = db.Column(db.Float, nullable=True, default=0)
    state = db.Column(db.Integer, nullable=False, default=10)

    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey("user_shop.id"), unique=True)
    license_id = db.Column(db.Integer, db.ForeignKey("shop_license.id"), unique=True)

    # 反向引用
    items = db.relationship("shop_items", backref=db.backref("shop"), uselist=True,
                            lazy="dynamic")

    def __repr__(self):
        return "<shop %r, shop_owner %r>" % (self.shop_name, self.shop_owner.name)


class shop_license(db.Model):
    __tablename__ = "shop_license"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idcard_name = db.Column(db.String(30), nullable=True)
    idcard_num = db.Column(db.String(18), nullable=True, unique=True)
    idcard_img = db.Column(db.LargeBinary, nullable=True)
    business_img = db.Column(db.LargeBinary, nullable=True)
    business_address = db.Column(db.String(100), nullable=True)
    business_name = db.Column(db.String(40), nullable=True)
    business_begin_time = db.Column(db.DateTime, default=datetime.now)
    business_end_time = db.Column(db.DateTime, nullable=True)
    business_num = db.Column(db.String(18), nullable=True, unique=True)
    service_img = db.Column(db.LargeBinary, nullable=True)
    service_address = db.Column(db.String(100), nullable=True)
    service_name = db.Column(db.String(40), nullable=True)
    service_begin_time = db.Column(db.DateTime, nullable=True)
    service_end_time = db.Column(db.DateTime, nullable=True)
    service_num = db.Column(db.String(18), nullable=True, unique=True)
    status = db.Column(db.Integer, nullable=True)
    add_time = db.Column(db.DateTime, default=datetime.now)

    # 反向引用
    shop = db.relationship("shop_info", backref=db.backref('shop_license'), uselist=False,
                           lazy="select")

    def __repr__(self):
        return "<shop_license %r>" % self.id


class shop_items(db.Model):
    __tablename__ = "shop_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_img = db.Column(db.LargeBinary, nullable=True)
    item_stock = db.Column(db.Integer, nullable=True)
    item_cate = db.Column(db.Integer, nullable=True)
    item_price = db.Column(db.Integer, nullable=True)
    item_introduction = db.Column(db.String(128), nullable=True)
    state = db.Column(db.Integer, nullable=False, default=10)

    # 外键
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id"), nullable=False)

