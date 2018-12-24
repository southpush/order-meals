# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import jsonify,request
from .. import db
from app.models.admin import Admin
from app.models.user import user_personal,ctd


class UserGet(Resource):
    def get(self):
        page = request.args.get('page')
        pag = user_personal.query.filter().order_by(user_personal.id.desc()).paginate(page=page,per_page=8)
        # for i in list:
        #     print(list[i])
        lists = pag.imems
        total_page = pag.pages

        l = []
        for i in lists:
            l.append(ctd(i))

        return jsonify(l)



