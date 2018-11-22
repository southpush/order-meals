# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config
from flask_restful import Api

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
api = Api()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    api.init_app(app)

    # 注册main的蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册api_1_0的蓝图
    from .api_1_0 import api_1_0 as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint)

    # 附加路由和自定义的错误页面

    return app

