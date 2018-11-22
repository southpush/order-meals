# -*- coding: utf-8 -*-
from flask import Blueprint

api_1_0 = Blueprint("api_1_0", __name__, url_prefix="/api")


from . import api_user, errors, api_route

