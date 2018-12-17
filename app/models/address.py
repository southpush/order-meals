# coding: utf-8
from .. import db


class Region(db.Model):
    __tablename__ = 'region'

    region_id = db.Column(db.Integer, index=True, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False, index=True)
    region_name = db.Column(db.String(64, 'utf8mb4_unicode_ci'), nullable=False)
    region_type = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return "<Region %r, id=%r>" % (self.region_name, self.region_id)


class address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.Integer, nullable=False)
    city = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)

    detailed = db.Column(db.String(64), nullable=False)
    contact_phone = db.Column(db.String(11), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)

    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user_personal.id"))

    def get_address_dict(self):
        info_dict = {
            "province": Region.query.filter_by(region_id=self.province).first().region_name,
            "city": Region.query.filter_by(region_id=self.city).first().region_name,
            "area": Region.query.filter_by(region_id=self.area).first().region_name,
            "detailed": self.detailed
        }
        return info_dict

    def get_address_str(self):
        province = Region.query.filter_by(region_id=self.province).first().region_name
        city = Region.query.filter_by(region_id=self.city).first().region_name
        area = Region.query.filter_by(region_id=self.area).first().region_name
        return province+city+area+self.detailed

    def __repr__(self):
        return "<address %r>" % self.id

