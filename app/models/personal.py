# -*- coding: utf-8 -*-
from .. import db


class comment(db.Model):
    __tablename__ = "user_comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)

    # 外鍵
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<comment id = %r>" % self.id

