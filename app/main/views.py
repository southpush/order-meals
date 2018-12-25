# -*- coding: utf-8 -*-

from flask import render_template
#导入蓝本 main
from . import main


@main.route("/", methods=["POST", "GET"])
def get_index():
    return render_template("myindex.html")


@main.route("/admin", methods=["POST", "GET"])
def get_admin():
    return render_template("index.html")







