# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 11:12
# @Author  : Min
# @Version : 1.0
from flask_restful import Resource
from flask import request
from app.models.shop import shop_info, shop_license, Status, ctd_shop
from app.models.user import user_shop
from app.api_1_0.response import general_response
from sqlalchemy import and_
from app.utils.login import permission_required
from app.models.role import Permission
from flask_login import login_required
from app.db.user_db import update_in_db


# 商铺信息获取
class ShopInfoGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        owner_id = request.args.get('id')
        print(owner_id)
        list = shop_info.query.filter_by(owner_id=owner_id).all()
        # 为空返回1006
        if len(list) == 0:
            return general_response(err_code=1006)
        else:
            # 有则根据商家id查找
            Shop_info = shop_info.query.filter_by(owner_id=owner_id).first()

        result = ctd_shop(Shop_info)
        return general_response(info={"shopinfo": result})


# 商家信息审核通过
class ShopPass(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        # 商铺信息通过审核
        id = request.args.get("id")
        Shop_info = shop_info.query.filter_by(id=id).first()
        # 如果状态为未审核或不通过 则进行审核
        if Shop_info.status == Status.IN_SHOP or Shop_info.status == Status.EXAMINE_NOT_PASS:
            status = Status.EXAMINE_PASS
            try:
                # 修改对应状态信息
                what = shop_info.query.filter_by(id=id)
                what.update({'status': status})
                update_in_db(what)
                print('success')
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)
        result = ctd_shop(Shop_info)
        return general_response(info={'result': result})


class ShopNotPass(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN , Permission.ADMINISTER])
    def post(self):
        # 商铺信息不通过审核
        id = request.args.get("id")
        Shop_info = shop_info.query.filter_by(id=id).first()
        # 如果状态为未审核 则进行审核
        if Shop_info.status == Status.IN_SHOP:
            status = Status.EXAMINE_NOT_PASS
            try:
                # 修改对应状态
                what = shop_info.query.filter_by(id=id)
                what.update({'status': status})
                update_in_db(what)
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)
        result = shop_info.get_shop_info(Shop_info)
        return general_response(info={'result': result})


class ShopInPass(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        id = request.args.get('id')
        Shop_info = shop_info.query.filter_by(id=id).first()
        license_id = Shop_info.license_id
        Shop_license = shop_license.query.filter_by(id=license_id).first()
        if Shop_info.status == Status.EXAMINE_PASS and Shop_license.status == Status.LICENSE_PASS:
            status = Status.PASS
            try:
                what = shop_info.query.filter_by(id=id)
                what.update({'status': status})
                update_in_db(what)
                print('success')
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)
        result = ctd_shop(Shop_info)
        return general_response(info={'result': result})


#
class ShopGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        name = request.args.get('name')
        phone = request.args.get('phone')
        page = int(request.args.get('page'))
        # 根据手机号码查询对应商家信息
        list = user_shop.query.filter(user_shop.phone.like("%" + phone + "%") if phone is not None else"").all()
        owner_id = []
        if list is None:
            owner_id = ''
        else:
            for i in list:
                owner_id.append(i.id)
        # 根据商家id查找对应商铺信息
        pag = shop_info.query.filter(
            and_(shop_info.owner_id.in_(owner_id),
                 shop_info.shop_name.like("%" + name + "%") if name is not None else "")
        ).order_by(shop_info.id.asc()).paginate(page=page, per_page=1)

        lists = pag.items
        total_page = pag.pages

        # total_page等于0时 返回1008
        if total_page == 0:
            return general_response(err_code=1008)
        else:
            l = []
            for i in lists:
                l.append(ctd_shop(i))
            return general_response(info={'list': l, "total_page": total_page})
