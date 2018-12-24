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
    status = db.Column(db.Integer, nullable=False, default=10)
    total_items = db.Column(db.Integer, nullable=False, default=0)

    box_price = db.Column(db.Float, nullable=False, default=0)
    send_cost = db.Column(db.Float, nullable=False, default=0)

    # 收货信息
    address_str = db.Column(db.String(200), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)
    contact_phone = db.Column(db.String(11), nullable=False)

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id", ondelete="CASCADE"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)

    # 反向引用
    items = db.relationship("order_items", backref=db.backref("order"), lazy="dynamic",
                            cascade="all, delete-orphan", passive_deletes=True)
    charge_back_info = db.relationship("charge_back_info", backref=db.backref("order"), uselist=False,
                                       lazy="select", cascade="all, delete-orphan", passive_deletes=True)

    def get_order_dict_personal(self):
        if self.status == order_status.waiting_for_pay:
            if (datetime.now() - self.create_time).days > 0 or (datetime.now() - self.create_time).seconds > 800:
                self.status = order_status.shut_down_over_payment_time
                db.session.commit()
        elif self.status == order_status.waiting_for_receive:
            if (datetime.now() - self.pay_time).days > 0 or (datetime.now() - self.pay_time).seconds > 3600:
                self.status = order_status.shut_down_shop_no_receive
                db.session.commit()
        elif self.status == order_status.waiting_for_delivery:
            if (datetime.now() - self.pay_time).days > 0 or (datetime.now() - self.pay_time).seconds > 7200:
                self.status = order_status.arrived
                db.session.commit()
        elif self.status == order_status.arrived:
            if (datetime.now() - self.pay_time).days > 2:
                self.status = order_status.completed
                db.session.commit()
        items_list = []
        for i in self.items.all():
            items_list.append(i.get_item_dict())
        info = {
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "pay_time": self.pay_time if not self.pay_time else self.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_price": self.total_price,
            "total_items_num": self.total_items,
            "status": self.status,
            "shop_name": self.shop.shop_name,
            "shop_id": self.shop.id,
            "items_list": items_list,
            "send_cost": self.send_cost,
            "box_price": self.box_price,
            "order_id": self.id,
            "order_address": self.address_str,
            "receiver": self.receiver,
            "contact_phone": self.contact_phone
        }
        return info

    def get_simple_dict_personal(self):
        if self.status == order_status.waiting_for_pay:
            if (datetime.now() - self.create_time).days > 0 or (datetime.now() - self.create_time).seconds > 800:
                self.status = order_status.shut_down_over_payment_time
                db.session.commit()
        elif self.status == order_status.waiting_for_receive:
            if (datetime.now() - self.pay_time).days > 0 or (datetime.now() - self.pay_time).seconds > 3600:
                self.status = order_status.shut_down_shop_no_receive
                db.session.commit()
        elif self.status == order_status.waiting_for_delivery:
            if (datetime.now() - self.pay_time).days > 0 or (datetime.now() - self.pay_time).seconds > 7200:
                self.status = order_status.arrived
                db.session.commit()
        elif self.status == order_status.arrived:
            if (datetime.now() - self.pay_time).days > 2:
                self.status = order_status.completed
                db.session.commit()
        # elif self.status == order_status.w
        # db.session.commit()
        info = {
            "create_time": self.create_time,
            "total_price": self.total_price,
            "total_items_num": self.total_items,
            "shop_name": self.shop.shop_name,
            "status": self.status,
            "first_item": self.items.first().item_name,
            "order_id": self.id,
            "shop_image_name": self.shop.shop_img_name
        }
        return info

    def get_order_dict_shop(self):
        items_list = []
        for i in self.items:
            items_list.append(i.get_item_dict())
        info = {
            "pay_time": self.pay_time,
            "address": self.address_str,
            "receiver": self.receiver,
            "contact_phone": self.contact_phone,
            "total_price": self.total_price,
            "total_items_num": self.total_items,
            "status": self.status,
            "items_list": items_list
        }
        return info

    def count(self):
        items = self.items.all()
        self.total_items = len(items)
        for i in items:
            self.total_price += ((i.item_price + i.additional_costs) * i.item_num)
        self.total_price += self.send_cost + self.box_price
        self.total_price = round(self.total_price, 2)
        return self.total_items, self.total_price

    def __repr__(self):
        return "<order id = %r>" % self.id

    @property
    def status_info(self):
        return order_status.status_dict[int(self.status)]


class order_items(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_num = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_name = db.Column(db.String(20), nullable=False)
    specification_name = db.Column(db.String(15), nullable=True)
    additional_costs = db.Column(db.Float, nullable=False, default=0)

    # 外键
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)

    def get_item_dict(self):
        info = {
            "item_num": self.item_num,
            "item_name": self.item_name,
            "item_price": self.item_price,
            "item_id": self.item_id,
            "item_image_name": self.shop_item.item_image_name
        }
        if self.specification_name and self.additional_costs:
            info["specification_name"] = self.specification_name
            info["additional_costs"] = self.additional_costs
        return info

    def __repr__(self):
        return "<order items id = '%r'>" % self.id


class charge_back_info(db.Model):
    __tablename__ = "charge_back_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personal_reason = db.Column(db.String(300), nullable=False)
    shop_reason = db.Column(db.String(300), nullable=True)
    admin_reason = db.Column(db.String(300), nullable=True)

    # 外键
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)

    def get_charge_back_info_dict(self):
        info = {
            "charge_back_info_id": self.id,
            "personal_reason": self.personal_reason,
            "shop_reason": self.shop_reason,
            "admin_reason": self.admin_reason,
        }
        return info


class order_status:
    waiting_for_pay = 10
    waiting_for_receive = 11
    waiting_for_delivery = 20
    # 订单到达
    arrived = 30
    personal_cancel = 40
    shop_refuse = 41
    # 5开头的状态都算在订单关闭里了
    shut_down_no_pay = 50
    shut_down_return_to_personal = 51
    shut_down_return_to_shop = 52
    shut_down_over_payment_time = 53
    shut_down_shop_no_receive = 54
    # 订单正常完成的
    completed = 60

    status_dict = {
        10: "waiting_for_pay",
        11: "waiting_for_receive",
        20: "waiting_for_delivery",
        30: "arrived",
        40: "personal_cancel",
        41: "shop_refuse",
        50: " shut_down_no_pay",
        51: "shut_down_return_to_personal",
        52: "shut_down_return_to_shop",
        52: "shut_down_over_payment_time",
        60: "completed"
    }
