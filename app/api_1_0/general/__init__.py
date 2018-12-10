# -*- coding: utf-8 -*-
from flask import Blueprint

api_1_0_general = Blueprint("api_1_0_general", __name__, url_prefix="/api/v1.0")

from app.api_1_0.general import api_route