# -*- coding: utf-8 -*-
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.glovar import secret_key


class user_personal(db.Model):
    __tablename__ = "user_personal"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    head_img = db.Column(db.LargeBinary(length=2048), nullable=True)
    nickname = db.Column(db.String(64), nullable=True)

    # 反向引用
    address = db.relationship("user_address", backref=db.backref("user"), uselist=True,
                              lazy="dynamic")
    shopping_car = db.relationship("shopping_car", backref=db.backref("user"), uselist=True,
                                   lazy="dynamic")
    comment = db.relationship("comment", backref=db.backref("user"), uselist=True,
                              lazy="dynamic")
    order = db.relationship("orders", backref=db.backref("user"), uselist=True,
                            lazy="dynamic")

    # 将password设置成不可读属性
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # 将password设置成只可写属性，参数传入password，然后将password的散列值存起来
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # user的password验证传入password，用werkzeug的函数来验证
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成认证token
    def generate_auth_token(self, expiration=7200):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({"id": self.id, "role": 0})

    # 确认token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None
        if data["role"]:
            return None
        user = user_personal.query.get(data["id"])
        return user

    def __repr__(self):
        return "<User_personal %r>" % self.nickname


class user_shop(db.Model):
    __tablename__ = "user_shop"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    openid = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # shop_info 的映射
    shop = db.relationship("shop_info", backref=db.backref("shop_owner"), uselist=False,
                           lazy="select")

    # 将password设置成不可读属性
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # 将password设置成只可写属性，参数传入password，然后将password的散列值存起来
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # user的password验证传入password，用werkzeug的函数来验证
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

        # 生成认证token
    def generate_auth_token(self, expiration=7200):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({"id": self.id, "role": 1})

    # 确认token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None
        if not data["role"]:
            return None
        user = user_personal.query.get(data["id"])
        return user

    def __repr__(self):
        return "<User_shop %r>" % self.name



