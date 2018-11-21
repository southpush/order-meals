# -*- coding: utf-8 -*-
# 创建蓝本

from flask import Blueprint

main = Blueprint("main", __name__)

from . import views, errors
