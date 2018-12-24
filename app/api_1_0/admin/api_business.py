# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 17:53
# @Author  : Min
# @Version : 1.0
from flask_restful import Resource
from flask import request
from app.models.user import user_shop, ctd_usershop
from sqlalchemy import and_
from app.utils.response import general_response
from app.utils.login import permission_required
from app.models.role import Permission
from flask_login import login_required


# 查询商家用户信息
class BusinessGet(Resource):
    # 权限：用户管理员/商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.USERADMIN, Permission.ADMINISTER])
    def get(self):
        page = int(request.args.get('page'))
        # print(current_user.name)
        name = request.args.get('name')
        phone = request.args.get('phone')
        # if name == "" and phone== "":
        #     all_results = user_personal.query.all()

        # 分页关键字查询
        pag = user_shop.query.filter(
            and_(user_shop.phone.like("%" + phone + "%") if phone is not None else "",
                 user_shop.nickname.like("%" + name + "%") if name is not None else "")
        ).order_by(user_shop.id.asc()).paginate(page=page, per_page=1)

        lists = pag.items
        total_page = pag.pages  # 总页数

        # total_page等于0时：
        if total_page == 0:
            return general_response(err_code=1008)
        else:
            l = []
            for i in lists:
                l.append(ctd_usershop(i))
            return general_response(info={'lists': l, "total_page": total_page})
