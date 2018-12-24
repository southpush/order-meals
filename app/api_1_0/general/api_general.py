# -*- coding: utf-8 -*-
import os

from flask import request, Response
from flask_restful import Resource, reqparse

from app.api_1_0.response import general_response
from app.db.user_db import update_in_db
from app.main.auth import login_required_personal, login_required_shop
from app.models.address import Region


class region(Resource):
    def get(self, parent_id):
        region_list = Region.query.filter_by(parent_id=parent_id).all()
        if not region_list:
            return general_response(err_code=410, status_code=404)
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
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

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
        return general_response({"success": user.head_image_name})


class user_shop_head_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/user_shop_head/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

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
        return general_response({"success": user.head_image_name})


class shop_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/shop_image/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

    @login_required_shop()
    def post(self, user):
        path = "app/static/shop_image/"
        file = request.files.get("file")
        shop = user.shop
        if not shop:
            return general_response(err_code=303, status_code=404)
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if shop.shop_img_name:
            if not shop.shop_img_name == "default.jpg":
                try:
                    os.remove(path + user.head_image_name)
                except FileNotFoundError as e:
                    print(e.__repr__())

        filename = str(shop.id) + file.filename
        file.save(path+filename)
        shop.shop_img_name = filename
        update_in_db(shop)
        return general_response({"success": shop.shop_img_name})


class shop_item_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/shop_item_image/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

    @login_required_shop()
    def post(self, user):
        data = reqparse.RequestParser()
        data.add_argument("item_id", type=int)
        item_id = data.parse_args()["item_id"]
        path = "app/static/shop_item_image/"
        file = request.files.get("file")
        item = user.shop.items.filter_by(id=item_id).first()
        if not item:
            return general_response(err_code=406, status_code=404)
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if item.item_image_name:
            try:
                os.remove(path + user.head_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(item.id) + file.filename
        file.save(path + filename)
        item.item_image_name = filename
        update_in_db(item)
        return general_response({"success": item.item_image_name})


class shop_license_idcard_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/shop_license_idcard/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

    @login_required_shop()
    def post(self, user):
        license = user.shop.license
        if not license:
            return general_response(err_code=708)
        path = "app/static/shop_license_idcard/"
        file = request.files.get("file")
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576*3:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if license.idcard_image_name:
            try:
                os.remove(path + license.idcard_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(user.id) + file.filename
        file.save(path+filename)
        license.idcard_image_name = filename
        update_in_db(license)
        return general_response({"license_idcard_image_name": license.idcard_image_name})


class shop_license_business_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/shop_license_business/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

    @login_required_shop()
    def post(self, user):
        license = user.shop.license
        if not license:
            return general_response(err_code=708)
        path = "app/static/shop_license_business/"
        file = request.files.get("file")
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576*3:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if license.business_image_name:
            try:
                os.remove(path + license.business_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(user.id) + file.filename
        file.save(path+filename)
        license.business_image_name = filename
        update_in_db(license)
        return general_response({"license_business_image_name": license.business_image_name})


class shop_license_service_image(Resource):
    def get(self, image_name):
        try:
            f = open("app/static/shop_license_service/" + image_name, "rb")
            file = f.read()
            resp = Response(file, mimetype="image/jpeg")
            return resp
        except FileNotFoundError as e:
            print(e.__repr__())
            return general_response(err_code=409, status_code=404)
        except TypeError as e:
            print(e.__repr__())
            return general_response(err_code=702, status_code=400)

    @login_required_shop()
    def post(self, user):
        license = user.shop.license
        if not license:
            return general_response(err_code=708)
        path = "app/static/shop_license_service/"
        file = request.files.get("file")
        if not file:
            return general_response(err_code=101, status_code=400)
        if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return general_response(err_code=108, status_code=400)
        file.seek(0, 2)
        if file.tell() > 1048576*3:
            return general_response(err_code=107, status_code=403)
        file.seek(0)
        if license.service_image_name:
            try:
                os.remove(path + license.service_image_name)
            except FileNotFoundError as e:
                print(e.__repr__())

        filename = str(user.id) + file.filename
        file.save(path+filename)
        license.service_image_name = filename
        update_in_db(license)
        return general_response({"license_service_image_name": license.service_image_name})


