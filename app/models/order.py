# -*- coding: utf-8 -*-
from datetime import datetime

from .. import db


class orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    pay_time = db.Column(db.DateTime)
    wx_order_no = db.Column(db.String(32), nullable=True)
    total_price = db.Column(db.Float, nullable=False, default=0)
    state = db.Column(db.Integer, default=10)
    total_items = db.Column(db.Integer, nullable=False, default=0)

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id", ondelete="CASCADE"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)

    # 反向引用
    items = db.relationship("order_items", backref=db.backref("order"), lazy="dynamic"
                            , cascade="all, delete-orphan", passive_deletes=True)

    def get_order_dict(self):
        items_list = []
        for i in self.items:
            items_list.append(i.get_item_dict())
        info = {
            "create_time": self.create_time,
            "pay_time": self.pay_time,
            "wx.order_no": self.wx_order_no,
            "total_price": self.total_price,
            "total_items_num": self.total_items,
            "state": self.state,
            "shop_name": self.shop.shop_name,
            "shop_id": self.shop.id,
            "items_list": items_list
        }
        return info

    def get_simple_dict(self):
        info = {
            "create_time": self.create_time,
            "total_price": self.total_price,
            "total_items_num": self.total_items,
            "shop_name": self.shop.shop_name,
            "state": self.state,
            "first_item": self.items.first().item_name
        }
        return info

    def count(self):
        items = self.items.all()
        self.total_items = len(items)
        for i in items:
            self.total_price += (i.item_price * i.item_num)
        self.total_price = round(self.total_price, 2)
        return self.total_items, self.total_price

    def __repr__(self):
        return "<comment id = %r>" % self.id


class order_items(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_num = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_name = db.Column(db.String(20), nullable=False)

    # 外键
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)

    def get_item_dict(self):
        info = {
            "item_num": self.item_num,
            "item_name": self.item_name,
            "item_price": self.item_price,
            "item_id": self.item_id
        }
        return info

    def __repr__(self):
        return "<order items id = '%r'>" % self.id
