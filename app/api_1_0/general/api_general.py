# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse

from app.db.user_db import get_img


class img(Resource):
    def get(self):
        data = reqparse.RequestParser()
        data.add_argument("img_id", type=int)
        imgget = get_img(img_id=data.parse_args()["img_id"])
        print("in img")
        print(imgget)
        return imgget