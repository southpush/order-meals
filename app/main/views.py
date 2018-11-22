# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import render_template, request, jsonify

from . import main


@main.route("/", methods=["POST", "GET"])
def get_task():
    env = "hello, world"
    return jsonify({"data:": env, "id": "hello a "})



