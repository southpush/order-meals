# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import jsonify
from .. import db
from ..models.User import User


class getUser(Resource):
    def get(self):
        user = User(name="testname2")
        db.session.add(user)
        db.session.commit()
        return jsonify({"data:": "hello !"})


