# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_restful import Api
from flask_login import LoginManager


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.session_protection='strong'
loginmanager.login_view='main.user'
loginmanager.login_message = "请先登录或者注册"
api = Api()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    api.init_app(app)
    loginmanager.init_app(app)

    # 注册main的蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册api_1_0_personal的蓝图
    from .api_1_0.personal import api_1_0_personal as api_1_0_personal_blueprint
    app.register_blueprint(api_1_0_personal_blueprint)

    # 注册 admin 的蓝图
    from .api_1_0.admin import api_1_0_admin as api_1_0_admin_blueprint
    app.register_blueprint(api_1_0_admin_blueprint)

    # 注册 shop 的蓝图
    from .api_1_0.shop import api_1_0_shop as api_1_0_shop_blueprint
    app.register_blueprint(api_1_0_shop_blueprint)

    # 附加路由和自定义的错误页面

    return app

