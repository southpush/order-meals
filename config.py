# -*- coding: utf-8 -*-
import os
# 获取当前配置文件所在的路径
# basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "258741"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SUBJECT_PREFIX = '[今天吃什么]'
    MAIL_SENDER = 'pppppu <southpush@outlook.com>'
    ADMIN = os.environ.get("MAIL_USERNAME")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:258741@localhost:3307/development?charset=utf8"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:258741@localhost:3307/test?charset=utf8"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:258741@localhost:3307/production?charset=utf8"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

