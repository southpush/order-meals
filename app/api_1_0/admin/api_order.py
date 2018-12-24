# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 11:39
# @Author  : Min
# @Version : 1.0
from flask_restful import Resource
from flask import request
from app.models.shop import shop_info, ctd_shop_order
from app.models.order import orders, ctd_orders, charge_back_info, ctd_charge_back, order_status
from app.utils.response import general_response
from app.utils.login import permission_required
from app.models.role import Permission
from flask_login import login_required
from app.db.user_db import update_in_db


# 根据订单时间分页查询订单信息
class OrderGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        page = int(request.args.get('page'))
        starttime = request.args.get('starttime')
        endtime = request.args.get('endtime')
        # 分页查询
        pag = shop_info.query.filter().order_by(shop_info.id.asc()).paginate(page=page, per_page=1)
        lists = pag.items
        # print(lists)
        total_page = pag.pages
        # 总页数为空返回1008
        if total_page == 0:
            return general_response(err_code=1008)
        else:
            l = []
            # 时间信息的处理
            for i in lists:
                if starttime == '' and endtime == '':
                    start_time = '2000-01-01'
                    end_time = '2999-12-31'
                else:
                    start_time = starttime
                    end_time = endtime
                Orders = orders.query.filter_by(shop_id=i.id).filter(
                    orders.pay_time.between(start_time, str(end_time) + " 23:59:59")).all()

                l.append(ctd_shop_order(i, Orders))
            return general_response(info={'lists': l, "total_page": total_page})


# 用户列表的订单信息获取
class OrderUserGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.USERADMIN, Permission.ADMINISTER])
    def get(self):
        user_id = request.args.get('id')
        list = orders.query.filter_by(user_id=user_id).all()
        l = []
        if len(list) == 0:
            return general_response(err_code=1009)
        else:
            for i in list:
                l.append(ctd_orders(i))

        return general_response(info={"list": l})


# 商铺列表的订单信息获取
class OrderShopGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        shop_id = request.args.get('id')
        list = orders.query.filter_by(shop_id=shop_id).all()
        l = []
        if len(list) == 0:
            return general_response(err_code=1009)
        else:
            for i in list:
                l.append(ctd_orders(i))

        return general_response(info={"list": l})


# 退单订单获取
class OrderBackGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        page = int(request.args.get('page'))
        pag = orders.query.filter_by(status=order_status.shop_refuse).order_by(orders.id.asc()).paginate(page=page,
                                                                                                         per_page=1)
        lists = pag.items
        total_page = pag.pages
        if total_page == 0:
            return general_response(err_code=1008)
        else:
            l = []
            for i in lists:
                l.append(ctd_orders(i))
            return general_response(info={'list': l, "total_page": total_page})


# 退单信息获取
class ChargeBackGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        id = request.args.get('id')
        info = charge_back_info.query.filter_by(order_id=id).first()
        l = ctd_charge_back(info)

        return general_response(info={'result': l})


# 退单信息审核 同意退单
class ChargeBackPass(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        order_id = request.args.get('id')
        reason = request.args.get('reason')
        print(order_id)
        Orders = orders.query.filter_by(id=order_id).first()
        print(Orders)
        if Orders.status == order_status.shop_refuse:
            status = order_status.shut_down_return_to_personal
            try:
                w1 = orders.query.filter_by(id=order_id)
                w1.update({'status': status})
                w2 = charge_back_info.query.filter_by(order_id=order_id)
                w2.update({'admin_reason': reason})
                update_in_db(w1)
                update_in_db(w2)
                print('success')
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)

            result = ctd_orders(Orders)
            return general_response(info={'result': result})


# 退单信息审核 不同意退单
class ChargeBackNotPass(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def post(self):
        order_id = request.args.get('id')
        reason = request.args.get('reason')
        Orders = orders.query.filter_by(id=order_id).first()
        if Orders.status == order_status.shop_refuse:
            status = order_status.shut_down_return_to_shop
            try:
                w1 = orders.query.filter_by(id=order_id)
                w1.update({'status': status})
                w2 = charge_back_info.query.filter_by(order_id=order_id)
                w2.update({'admin_reason': reason})
                update_in_db(w1)
                update_in_db(w2)
                print('success')
            except Exception as e:
                # db.session.rollback()
                print('failed')
                print(e)

            result = ctd_orders(Orders)
            return general_response(info={'result': result})


# 根据订单时间的分页查询（已使用OrderGet 该方法无用）
class CountGet(Resource):
    # 权限：商铺管理员/超级管理员
    @login_required
    @permission_required([Permission.SHOPERADMIN, Permission.ADMINISTER])
    def get(self):
        page = int(request.args.get('page'))
        startime = request.args.get('starttime')
        endtime = str(request.args.get('endtime')) + ' 23:59:59'

        # Orders = orders.query.filter_by(id=id).first()
        if startime == '' and endtime == '':
            pag = orders.query.filter().paginate(page=page, per_page=1)
        else:
            pag = orders.query.filter(orders.pay_time.between(startime, endtime)).paginate(page=page, per_page=1)
        lists = pag.items
        total_page = pag.pages

        if total_page == 0:
            return general_response(err_code=1008)
        else:
            l = []
            for i in lists:
                l.append(ctd_orders(i))
            return general_response(info={'lists': l, "total_page": total_page})
