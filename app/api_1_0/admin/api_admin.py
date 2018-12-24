#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 10:43
# @Author  : Min
# @Version : 1.0
from flask_restful import Resource, reqparse
from flask import request, session
from app.utils.sms import send_sms, verification_code
from app import db
from app.models.admin import Admin, ctd, get_md5
from flask_login import login_user, current_user, logout_user, login_required
from app.utils.response import general_response
from app.models.role import Permission
from app.utils.login import permission_required
import re

parser = reqparse.RequestParser()


# 管理员登陆
class AdminLogin(Resource):
    def post(self):
        phone = request.args.get('admin_phone')
        adminpass = request.args.get('adminpass')

        # 手机号码或密码为空时：
        if phone == "" or adminpass == "":
            return general_response(err_code=1001)

        # 判断数据库中是否有该手机号码
        list = db.session.query(Admin).filter_by(admin_phone=phone).all()
        # 为空返回101错误
        if len(list) == 0:
            return general_response(err_code=101)
        else:
            # 判断该手机号码格式是否正确
            admin_phone = re.match(r"^1[35678]\d{9}$", phone)
            if not admin_phone:
                # print('手机号码不正确!')
                return general_response(err_code=1002)

        # 跟据手机号码查找admin的信息
        admin = Admin.query.filter_by(admin_phone=phone).first()
        # 输入密码是否正确
        if admin.verify_adminpass(adminpass):
            # 登录返回True，否则False
            if admin.is_authenticated:

                login_user(admin, True)
                print('Login')
                return general_response(info={"name": current_user.name})
        else:
            # 密码不正确返回err_code
            return general_response(err_code=1005)


# 管理员注册
class AdminRegister(Resource):
    def post(self):
        adminpass = request.args.get('adminpass')
        phone = request.args.get('admin_phone')
        role_id = request.args.get('role_id')  # 角色id
        v_code = request.args.get('v_code')  # 验证码

        # 手机号码或密码或角色id为空时：
        if phone == "" or adminpass == "" or role_id == "":
            return general_response(err_code=1001)
        # 验证码为空时：
        if v_code == "":
            return general_response(err_code=1003)

        # 判断数据库中是否有该手机号码
        list = db.session.query(Admin).filter_by(admin_phone=phone).all()
        # 为空返回103错误
        if len(list) != 0:
            return general_response(err_code=103)
        else:
            # 判断该手机号码格式是否正确
            admin_phone = re.match(r"^1[35678]\d{9}$", phone)
            # print(admin_phone)
            if not admin_phone:
                # print('手机号码不正确!')
                return general_response(err_code=1002)

        # 判断验证码是否正确
        if v_code != verification_code:
            return general_response(err_code=1004)
        else:
            admin = Admin(id=session.get('id'),
                          name=phone,
                          role_id=role_id,
                          adminpass=adminpass,
                          admin_phone=phone)
            # 添加一个新的Admin
            db.session.add(admin)
            login_user(admin)
            try:
                db.session.commit()
                print("注册成功")
                return general_response(info={"name": current_user.name})
            except Exception as e:
                db.session.rollback()
                print('注册失败')
                print(repr(e))


# 获取验证码
class GetCode(Resource):
    def get(self):
        phone = request.args.get('phone')

        # 手机号码为空时：
        if phone == "":
            return general_response(err_code=1001)
        else:
            # 判断数据库中是否有该手机号码
            list = db.session.query(Admin).filter_by(admin_phone=phone).all()
            # 为空返回103错误
            if len(list) != 0:
                return general_response(err_code=103)

            else:
                # 判断该手机号码格式是否正确
                admin_phone = re.match(r"^1[35678]\d{9}$", phone)
                if admin_phone:
                    print('手机号码正确!')
                    send_sms(phone)
                    return general_response(info={'result': 'send success'})
                else:
                    print('手机号码不正确!')
                    return general_response(err_code=1002)


# 管理员登出账号
class AdminLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        return general_response(info={'result': 'logout success'})


# 获取当前管理员信息
class AdminGet(Resource):
    @login_required
    def get(self):
        # id = request.args.get('id')
        # 根据当前管理员名字查找信息
        admin = Admin.query.filter_by(name=current_user.name).first()
        result = ctd(admin)

        return general_response(info={'result': result})


# 获取所有管理员信息
class AllAdminGet(Resource):
    @login_required
    @permission_required([Permission.ADMINISTER])
    def get(self):
        all_result = Admin.query.filter().order_by(Admin.role_id.asc()).all()
        l = []
        if len(all_result) == 0:
            return general_response(err_code=1008)
        else:
            for i in all_result:
                l.append(ctd(i))
            return general_response(info={'lists': l})


# 管理员修改密码
class AdminEditPassword(Resource):
    @login_required
    def post(self):
        admin = Admin.query.filter_by(name=current_user.name).first()
        adminpass = request.args.get('adminpass')
        newpass = request.args.get('newpass')
        new_pass = request.args.get('new_pass')
        if newpass == new_pass:
            try:
                # 如果确认密码正确
                if admin.verify_adminpass(adminpass):
                    # 新的加密后的密码为新输入密码的加密
                    admin_slat = get_md5(newpass)
                    try:
                        # print(admin_slat)
                        # 修改数据库对应列加密密码字段
                        db.session.query(Admin).filter_by(name=current_user.name).update({'admin_slat': admin_slat})
                        db.session.commit()
                        return general_response(info={'result': 'success'})
                    except Exception as e:
                        db.session.rollback()
                        print('failed')
                        print(e)
            except Exception as e:
                print(repr(e))


# 管理员修改个人信息
class AdminEdit(Resource):
    def post(self):
        # admin = Admin.query.filter_by(name=current_user.name).first()

        name = request.args.get('name')
        phone = request.args.get('phone')
        try:
            # print(db.session.query(Admin))
            db.session.query(Admin).filter_by(name=current_user.name).update({'name': name, 'admin_phone':phone})
            db.session.commit()
            print('success')
        except Exception as e:
            db.session.rollback()
            print('failed')
            print(e)
