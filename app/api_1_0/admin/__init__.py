#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 10:42
# @Author  : Min
# @Version : 1.0

from flask import Blueprint

api_1_0_admin = Blueprint("api_1_0_admin", __name__, url_prefix="/api_1_0")

from app.api_1_0.admin import api_route
from app.api_1_0 import api_user, errors