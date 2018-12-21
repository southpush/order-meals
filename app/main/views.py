# -*- coding: utf-8 -*-
from flask import jsonify, Response, render_template

from app.api_1_0.response import general_response
from . import main


@main.route("/", methods=["POST", "GET"])
def get_task():
    return render_template("index.html")




