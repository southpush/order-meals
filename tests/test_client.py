# -*- coding: utf-8 -*-
import sqlalchemy
import unittest
from app import create_app, db
from app.models.personal import user_address, comment, shopping_car
from app.models.user import user_personal, user_shop
from app.models.shop import shop_info, shop_items, shop_license
from app.models.order import order_items, orders


class FlaskClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.session.execute("set FOREIGN_KEY_CHECKS = 0;")
        db.drop_all()
        db.create_all()

        cls.client = cls.app.test_client(use_cookies=True)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    # 期待抛出指定类型错误的断言
    def test_add_user(self):
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            user1 = user_personal(openid="openid1", phone="phone1", password="cat",
                                  head_img=0, nickname="ppppu1")
            user2 = user_personal(openid="openid1", phone="phone2", password="cat",
                                  head_img=0, nickname="ppppu")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        # 最后要rollback让session回归pool
        db.session.rollback()

    # 测试用户和用户地址的关联
    def test_user_personal_and_user_address(self):
        user1 = user_personal(openid="openid1", phone="phone1", password="cat",
                              head_img=0, nickname="ppppu1")
        user2 = user_personal(openid="openid2", phone="phone2", password="cat",
                              head_img=0, nickname="ppppu")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        address1 = user_address(user_id=user1.id)
        address2 = user_address(user_id=user1.id)
        address3 = user_address(user_id=user2.id)

        db.session.add(address1)
        db.session.add(address2)
        db.session.add(address3)
        db.session.commit()

        a = set(user1.address.all())
        b = set([address1, address2])
        self.assertEqual(a, b)

    # 测试一个商铺用户只能有一家店
    def test_user_shop_only_one_shop(self):
        user = user_shop(name="pu_shop_user", openid="adfe", phone="sadf3ee", password="asdfe")
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(repr(e))
            db.session.rollback()
        shop1 = shop_info(shop_name="pu shop1", contact_name="pu", contact_phone="adfefa",
                          address="daf4efdva", owner_id=user.id)
        shop2 = shop_info(shop_name="pu shop2", contact_name="pu", contact_phone="adffa",
                          address="daf4efda", owner_id=user.id)
        db.session.add(shop1)
        db.session.add(shop2)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            db.session.commit()
        db.session.rollback()




















