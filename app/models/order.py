# -*- coding: utf-8 -*-
from datetime import datetime

from .. import db


class orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    pay_time = db.Column(db.DateTime)
    wx_order_no = db.Column(db.String(32), nullable=True)
    total_price = db.Column(db.Integer, nullable=True)
    state = db.Column(db.Integer, default=10)
    total_items = db.Column(db.Integer, nullable=False)

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id", ondelete="CASCADE"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)

    # 反向引用
    items = db.relationship("order_items", backref=db.backref("order"), lazy="dynamic"
                            , cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return "<comment id = %r>" % self.id


class order_items(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_num = db.Column(db.Integer, nullable=True)
    item_price = db.Column(db.Integer, nullable=True)

    # 外键
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<order items id = '%r'>" % self.id
