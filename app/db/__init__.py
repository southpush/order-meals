# -*- coding: utf-8 -*-
from flask import Blueprint

db_blueprint = Blueprint("api_1_0", __name__)


from . import user_db, shop_db
