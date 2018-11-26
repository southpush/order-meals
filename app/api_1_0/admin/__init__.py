# -*- coding: utf-8 -*-
from flask import Blueprint

api_1_0_admin = Blueprint("api_1_0_admin", __name__, url_prefix="/api/v1.0/admin")

from app.api_1_0.admin import api_route