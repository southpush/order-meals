# -*- coding: utf-8 -*-
import unittest

from app.db.user_db import add_user_personal
from app.models.user import user_shop, user_personal
from app import db


# 密码散列化测试
class UserModelTestCase(unittest.TestCase):
    # 测试是否生成password_hash
    def test_password_setter(self):
        user = user_personal(password="cat")
        self.assertTrue(user.password_hash is not None)

    # 测试password不可访问
    def test_no_password_getter(self):
        user = user_personal(password="cat")
        with self.assertRaises(AttributeError):
            user.password

    # 测试是否能正确验证密码
    def test_password_verification(self):
        user = user_personal(password='cat')
        self.assertTrue(user.verify_password("cat"))
        self.assertFalse(user.verify_password("dog"))

    # 测试两个相同密码之间的散列值不同
    def test_password_salts_are_random(self):
        user1 = user_personal(password='cat')
        user2 = user_personal(password='cat')
        self.assertTrue(user1.password_hash != user2.password_hash)

    # 测试token验证
    def test_token_verify(self):
        user = user_personal(openid="test_Token", phone="9372649573", nickname="testTokenName", password="cat")
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token()
        user_verify = user_personal.verify_auth_token(token)
        self.assertTrue(user == user_verify)
