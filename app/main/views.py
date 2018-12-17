# -*- coding: utf-8 -*-
from flask import jsonify, Response

from app.api_1_0.response import general_response
from . import main


@main.route("/", methods=["POST", "GET"])
def get_task():
    env = "hello, world"
    return jsonify({"data:": env, "id": "hello a "})


@main.route("/head-img/<image_id>", methods=["GET"])
def get_img_route(image_id):
    img2 = get_img(img_id=image_id)
    if img2:
        resp = Response(img2, mimetype="image/jpeg")
        return resp
    return general_response(err_code=401, status_code=404)



