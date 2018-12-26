# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 10:50
# @Author  : Min
# @Version : 1.0

from flask_restful import Resource
from flask import request
from app.models.user import user_personal,ctd
from sqlalchemy import and_
from app.api_1_0.response import general_response
from app.utils.login import permission_required
from flask_login import login_required
from app.models.role import Permission


class UserGet(Resource):
    def get(self):
        page = int(request.args.get('page'))
        print(page)
        pag = user_personal.query.filter().order_by(user_personal.id.asc()).paginate(page=page, per_page=5)
        # for i in list:
        #     print(list[i])
        lists = pag.items
        total_page = pag.pages

        l = []
        for i in lists:
            l.append(ctd(i))

        return general_response(info={'lists': l, "total_page": total_page})


# 关键字查询
class GetByKeyWord(Resource):
    # 权限：用户管理员/超级管理员
    @login_required
    @permission_required([Permission.USERADMIN , Permission.ADMINISTER])
    def get(self):
        page = int(request.args.get('page'))
        name = request.args.get('name')
        phone = request.args.get('phone')
        # if name == "" and phone== "":
        #     all_results = user_personal.query.all()

        pag = user_personal.query.filter(
            and_(user_personal.phone.like("%" + phone + "%") if phone is not None else "",
                 user_personal.nickname.like("%" + name + "%") if name is not None else "")
        ).order_by(user_personal.id.asc()).paginate(page=page,per_page=5)
        # print(pag)
        lists = pag.items
        # print(lists)
        total_page = pag.pages
        # print(total_page)
        # total_page等于0时：
        if total_page == 0 :
            return general_response(err_code=1008)
        else:
            l = []
            for i in lists:
                l.append(ctd(i))
            return general_response(info={'lists': l, "total_page": total_page})


# 删除用户列表
class DeleteUser(Resource):
    def post(self):
        id = request.args.get('id')
        try:
            user_personal.query.filter_by(id=id).delete()
            return general_response(info={'result': 'login success'})
        except Exception as e:
            print(repr(e))
            return general_response(err_code=2001)
