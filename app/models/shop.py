# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column

from app.models.address import Region
from .. import db


class shop_info(db.Model):
    __tablename__ = "shop_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(30), nullable=False, unique=True)
    shop_introduction = db.Column(db.Text, nullable=True)
    floor_send_cost = db.Column(db.Float, nullable=True, default=0)
    send_cost = db.Column(db.Float, nullable=True, default=0)
    notic = db.Column(db.String(200), nullable=True, default="")
    score = db.Column(db.Float, nullable=True, default=0)
    shop_img_name = db.Column(db.String(50), nullable=False, default="default.jpg")
    box_price = db.Column(db.Float, nullable=True, default=0)
    status = db.Column(db.Integer, nullable=False, default=10)

    # 商铺地址
    province = db.Column(db.Integer, nullable=False)
    city = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    detailed = db.Column(db.String(64), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    # 联系人
    contact = db.Column(db.PickleType)

    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey("user_shop.id", ondelete="CASCADE"), unique=True,
                         nullable=False)

    # 反向引用
    items = db.relationship("shop_items", backref=db.backref("shop"), uselist=True,
                            lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    license = db.relationship("shop_license", backref=db.backref("shop"), uselist=False,
                              lazy="select", cascade="all, delete-orphan", passive_deletes=True)
    item_category = db.relationship("item_category", backref=db.backref("shop"), uselist=True,
                                    lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    order = db.relationship("orders", backref=db.backref("shop"), uselist=True,
                            lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    favorites = db.relationship("favorites", backref=db.backref("shop"), uselist=True,
                                lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return "<shop %r>" % self.shop_name

    def get_shop_info(self):
        shop_dict = {
            "shop_name": self.shop_name,
            "shop_introduction": self.shop_introduction,
            "floor_send_cost": self.floor_send_cost,
            "send_cost": self.send_cost,
            "notic": self.notic,
            "score": self.score,
            "shop_img": self.shop_img_name,
            "box_price": self.box_price,
            "status": self.status,
            "contact": self.contact,
            "address_dict": self.get_address_dict(),
            "address_str": self.get_address_str(),
            "lat": self.lat,
            "lng": self.lng
        }
        return shop_dict

    def get_simple_shop_info(self):
        shop_dict = {
            "shop_id": self.id,
            "score": self.score,
            "shop_img_name": self.shop_img_name,
            "shop_name": self.shop_name,
            "send_cost": self.send_cost
        }
        return shop_dict

    def get_address_dict(self):
        info_dict = {
            "province": Region.query.filter_by(region_id=self.province).first().region_name,
            "city": Region.query.filter_by(region_id=self.city).first().region_name,
            "area": Region.query.filter_by(region_id=self.area).first().region_name,
            "detailed": self.detailed
        }
        return info_dict

    def get_address_str(self):
        try:
            province = Region.query.filter_by(region_id=self.province).first().region_name
            city = Region.query.filter_by(region_id=self.city).first().region_name
            area = Region.query.filter_by(region_id=self.area).first().region_name
        except AttributeError as e:
            print(e.__repr__())
            return False
        return province+city+area+self.detailed


class shop_license(db.Model):
    __tablename__ = "shop_license"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idcard_name = db.Column(db.String(30), nullable=False)
    idcard_num = db.Column(db.String(18), nullable=False, unique=True)
    idcard_image_name = db.Column(db.String(100), nullable=True)
    business_image_name = db.Column(db.String(100), nullable=True)
    business_address = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(40), nullable=False)
    business_begin_time = db.Column(db.DateTime, default=datetime.now)
    business_end_time = db.Column(db.DateTime, nullable=False)
    business_num = db.Column(db.String(18), nullable=False, unique=True)
    service_image_name = db.Column(db.String(100), nullable=True)
    service_address = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(40), nullable=False)
    service_begin_time = db.Column(db.DateTime, nullable=False)
    service_end_time = db.Column(db.DateTime, nullable=False)
    service_num = db.Column(db.String(18), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=10)
    add_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), unique=True, nullable=False)

    # 获取许可表的信息
    def get_license_dict(self):
        info = {
            "idcard_name": self.idcard_name,
            "idcard_num": self.idcard_num,
            "idcard_image_name": self.idcard_image_name,
            "business_image_name": self.business_image_name,
            "business_address": self.business_address,
            "business_name": self.business_name,
            # 开始时间和结束时间只到年月日
            "business_begin_time": self.business_begin_time.strftime("%Y-%m-%d %H:%M:%S"),
            "business_end_time": self.business_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "business_num": self.business_num,
            "service_image_name": self.service_image_name,
            "service_address": self.service_address,
            "service_name": self.service_name,
            "service_begin_time": self.service_begin_time.strftime("%Y-%m-%d %H:%M:%S"),
            "service_end_time": self.service_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "service_num": self.service_num,
            "status": self.status,
            "add_time": self.add_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return info

    def __repr__(self):
        return "<shop_license %r>" % self.id


class shop_items(db.Model):
    __tablename__ = "shop_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(20), nullable=False)
    item_sales = db.Column(db.Integer, nullable=False, default=0)
    item_stock = db.Column(db.Integer, nullable=False, default=0)
    item_price = db.Column(db.Float, nullable=False, default=0)
    item_introduction = db.Column(db.String(128), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    item_image_name = db.Column(db.String(100), nullable=True)

    # 外键
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)  # type: Column
    item_category_id = db.Column(db.Integer, db.ForeignKey("item_category.id", ondelete="CASCADE"), nullable=False)

    # 反向引用
    specification = db.relationship("item_specification", backref=db.backref("item"), uselist=True,
                                    lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    order_item = db.relationship("order_items", backref=db.backref("shop_item"), uselist=True,
                                    lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)

    def get_item_detail(self):
        specification_list = []
        for i in self.specification.all():
            specification_list.append(i.get_specification_dict())
        item_dict = {
            "item_name": self.item_name,
            "shop_item_id": self.id,
            "item_sales": self.item_sales,
            "item_stock": self.item_stock,
            "item_price": self.item_price,
            "item_introduction": self.item_introduction,
            "item_image_name": self.item_image_name,
            "specification_list": specification_list,
            "category_id": self.item_category_id
        }
        return item_dict

    def __repr__(self):
        return "<shop_items %r, id %r, belong %r>" % (self.item_name, self.id, self.shop.shop_name)


class item_category(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(10), nullable=False)

    # 外键
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_info.id", ondelete="CASCADE"), nullable=False)

    # 反向引用
    items = db.relationship("shop_items", backref=db.backref("category"), uselist=True,
                            lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return "<item_category %r, belong shop %r>" % (self.category_name, self.shop)


class item_specification(db.Model):
    __tablename__ = "item_specification"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specification_name = db.Column(db.String(15), nullable=False)
    additional_costs = db.Column(db.Float, nullable=False, default=0)

    # 外键
    item_id = db.Column(db.Integer, db.ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)

    def get_specification_dict(self):
        info = {
            "specification_id": self.id,
            "specification_name": self.specification_name,
            "additional_costs": self.additional_costs
        }
        return info

    def __repr__(self):
        return "<item_specification %r, belong item_id %r>" % (self.specification_name, self.item.id)

