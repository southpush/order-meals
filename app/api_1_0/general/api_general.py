# -*- coding: utf-8 -*-
import os

from flask import request, Response
from flask_restful import Resource

from app.api_1_0.response import general_response
from app.db.user_db import update_in_db
from app.main.auth import login_required_personal, login_required_shop
from app.models.address import Region


class region(Resource):
    def get(self, parent_id):
        region_list = Region.query.filter_by(parent_id=parent_id).all()
        region_dict = {}
        for a in region_list:
            region_dict[a.region_name] = a.region_id
        return general_response(info=region_dict)


class user_personal_head_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/user_personal_head/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)

    @login_required_personal()
    def post(self, user):
        path = "app/static/user_personal_head/"
        file = request.files.get("file")
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if user.head_image_name:
            try:
                os.remove(path + user.head_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(user.id) + file.filename
        file.save(path+filename)
        user.head_image_name = filename
        update_in_db(user)
        return general_response({"success": filename})


class user_shop_head_image(Resource):
    def get(self, image_name):
        with open("app/static/user_shop_head/" + image_name, "rb") as f:
            file = f.read()
        resp = Response(file, mimetype="image/jpeg")
        return resp

    @login_required_shop()
    def post(self, user):
        path = "app/static/user_shop_head/"
        file = request.files.get("file")
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if user.head_image_name:
            try:
                os.remove(path + user.head_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(user.id) + file.filename
        file.save(path+filename)
        user.head_image_name = filename
        update_in_db(user)
        return general_response({"success": filename})


