# -*- coding: utf-8 -*-
from flask import Blueprint

api_1_0_personal = Blueprint("api_1_0_personal", __name__, url_prefix="/api/v1.0/personal")

from app.api_1_0.personal import api_route