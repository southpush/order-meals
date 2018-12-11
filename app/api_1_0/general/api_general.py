# -*- coding: utf-8 -*-
from flask import request, make_response, Response
from flask_restful import Resource, reqparse

from app.api_1_0.response import general_response
from app.db.user_db import get_img, add_in_db
from app.models.user import head_img


class img(Resource):
    def get(self, image_id):
        img2 = get_img(img_id=image_id)
        if img2:
            resp = Response(img2, mimetype="image/jpeg")
            return resp
        return general_response(err_code=401, status_code=404)

    def post(self):
        file = request.files.get("file")
        file.seek(0, 2)
        if file.tell() > 1048576:
            return general_response(err_code=107, status_code=403)
        if file:
            file.seek(0)
            img = head_img(img=file.stream.read())
        else:
            return general_response(err_code=101, status_code=400)
        if add_in_db(img):
            return general_response(info={"img_id": img.id})
        return general_response(err_code=105, status_code=400)
