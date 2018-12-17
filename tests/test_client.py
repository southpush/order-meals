# -*- coding: utf-8 -*-
import unittest
from app import create_app, db
from app.models.address import address, Region



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

    def test_add_address(self):
        pass



















