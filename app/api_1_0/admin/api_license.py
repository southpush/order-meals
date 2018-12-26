# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 15:05
# @Author  : Min
# @Version : 1.0
from flask_restful import Resource
from flask import request

from app.models.shop import shop_license, ctd_license, Status, shop_info
from app.api_1_0.response import general_response
from app.utils.login import permission_required
from app.models.role import Permission
from flask_login import login_required
from app.db.user_db import update_in_db


# 商铺许可证信息获取
class ShopLicenseGet(Resource):
    @login_required
    # 权限：商铺管理员/超级管理员
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        id = request.args.get('id')
        # 数据库中是否有对应id的许可证信息
        list = shop_license.query.filter_by(id=id).all()
        # 为空返回1007
        if len(list) == 0:
            return general_response(err_code=1007)
        else:
            # 有则根据id查询
            Shop_license = shop_license.query.filter_by(id=id).first()
            result = ctd_license(Shop_license)

        return general_response(info={"license": result})


# 许可证审核通过
class LicensePass(Resource):
    @login_required
    # 权限：商铺管理员/超级管理员
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        # 通过审核
        id = request.args.get("id")
        Shop_license = shop_license.query.filter_by(id=id).first()
        shop_id = Shop_license.shop_id
        Shop_info = shop_info.query.filter_by(id=shop_id).first()
        # 如果status为未审核或不通过 则进行审核
        if Shop_license.status != Status.LICENSE_PASS:
            status = Status.LICENSE_PASS
            if Shop_info.status == Status.EXAMINE_PASS:
                status = Status.PASS
                shop_info.query.filter_by(id=shop_id).update({"status": status})
        try:
            # 审核通过，修改对应status
            what = shop_license.query.filter_by(id=id)
            what.update({'status': status})
            update_in_db(what)
            print('success')
        except Exception as e:
            # db.session.rollback()
            print('failed')
            print(e)
        result = ctd_license(Shop_license)
        return general_response(info={'result': result})


# 许可证审核不通过
class LicenseNotPass(Resource):
    @login_required
    # 权限：商铺管理员/超级管理员
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        # 不通过审核
        id = request.args.get("id")
        Shop_license = shop_license.query.filter_by(id=id).first()
        # 如果status为10 则进行审核
        if Shop_license.status == Status.IN_EXAMINE:
            status = Status.LICENSE_NOT_PASS
            try:
                # 审核不通过，修改对应status
                what = shop_license.query.filter_by(id=id)
                # shop_license.query.filter_by(id=id).update({'status': status})
                what.update({'status': status})
                update_in_db(what)
                print('success')
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)
        result = ctd_license(Shop_license)
        return general_response(info={'result': result})
