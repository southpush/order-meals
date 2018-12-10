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
    notic = db.Column(db.String(200), nullable=True, default="")
    score = db.Column(db.Float, nullable=True, default=0)
    shop_img = db.Column(db.LargeBinary, nullable=True)
    box_price = db.Column(db.Float, nullable=True, default=0)
    state = db.Column(db.Integer, nullable=False, default=10)

    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey("user_shop.id", ondelete="CASCADE"), unique=True,
                         nullable=False)

    # 反向引用
    items = db.relationship("shop_items", backref=db.backref("shop"), uselist=True,
                            lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    license = db.relationship("shop_license", backref=db.backref("shop"), uselist=False,
                              lazy="select", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return "<shop %r>" % self.shop_name

    def get_shop_info(self):
        shop_dict = {
            "shop_name": self.shop_name,
            "shop_introduction": self.shop_introduction,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "geocoding": self.geocoding,
            "address": self.address,
            "floor_send_cost": self.floor_send_cost,
            "send_cost": self.send_cost,
            "notic": self.notic,
            "score": self.score,
            "shop_img": self.shop_img,
            "box_price": self.box_price,
            "state": self.state,
        }
        return shop_dict


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

    # 外键
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), unique=True, nullable=False)

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
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)

