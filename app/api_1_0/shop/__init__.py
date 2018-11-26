# -*- coding: utf-8 -*-
from flask import Blueprint

api_1_0_shop = Blueprint("api_1_0_shop", __name__, url_prefix="/api/v1.0/shop")

from app.api_1_0.shop import api_route