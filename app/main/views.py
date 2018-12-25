# -*- coding: utf-8 -*-
from flask import jsonify, Response, render_template

from app.db.user_db import update_in_db
from . import main

from flask import render_template, redirect, url_for, session
#导入蓝本 main
from . import main
from app import db
from .forms import Edit,Login,Register,Phone
from flask_login import login_required, login_user, current_user,logout_user
from app.models.admin import  Admin,get_md5
from app.models.role import Permission
from app.utils.login import admin_required, permission_required
from app.utils.sms import send_sms,verification_code


@main.route("/", methods=["POST", "GET"])
def get_index():
    return render_template("myindex.html")


# 整合的代码
@main.route('/phone',methods=['GET', 'admin'])
def sms():
    form = Phone()
    if form.validate_on_submit():
        phone = form.phone.data
        send_sms(phone)
        print(form.v_code.data)
        print(verification_code)
        print(form.v_code.data == verification_code)
        if form.v_code.data == verification_code:

            return redirect(url_for('main.register'))
    return render_template("index.html", form=form)


@login_required
@main.route("/index", methods =["GET", "admin"])
def index():
    return "hello"

@login_required
@main.route("/edit", methods =['GET', 'admin'])
def edit():
    form = Edit()
    admin = Admin.query.filter_by(name=current_user.name).first()
    try:
        if form.validate_on_submit():#判断request是个带admin数据，且数据符合表单定义要求
            if admin is not None and admin.verify_adminpass(form.adminpass.data):
                newpass = get_md5(form.newpass.data)
                # db.session.update(admin)

                try:
                    print(form.newpass.data)

                    # print(db.session.query(Admin))
                    what = Admin.query.filter_by(name=current_user.name)
                    db.session.query(Admin).filter_by(name=current_user.name).update({'admin_slat': newpass})
                    what.update({'admin_slat': newpass})


                    update_in_db(what)
                    print('success')
                    return redirect(url_for("main.index"))
                except Exception as e:
                    # db.session.rollback()
                    print('failed')
                    print(e)
        return render_template("edit.html", form = form)
    except Exception as e:
        print(e)


# 登录
@main.route('/login', methods=['GET', 'admin'])
def login():
    form = Login()
    admin = Admin.query.filter_by(name=form.name.data).first()
    if form is None:
        print('shuold input name and password')
    elif form.validate_on_submit():  # 判断request是个带admin数据，且数据符合表单定义要求
        if admin is not None and admin.verify_adminpass(form.adminpass.data):
            try:
                print(admin.role.permission)
                print(Permission.ADMINISTER)
                if admin.is_authenticated: #登录返回True，否则False
                    try:

                        if admin.role.permission == Permission.ADMINISTER:
                            login_user(admin, True)
                            print('Admin Login')
                            return redirect(url_for("main.admin_only"))

                        elif admin.role.permission == Permission.USERADMIN:
                            login_user(admin, True)
                            print('UserAdmin Login')
                            return redirect(url_for("main.useradmin_only"))

                        elif admin.role.permission == Permission.SHOPERADMIN:
                            login_user(admin, True)
                            print('ShoperAdmin Login')
                            return redirect(url_for("main.shoperadmin_only"))
                    except Exception as e:
                        print(e)

                else:
                    logout_user()
                    print('User Logout')
                    return redirect(url_for('main.index'))
            except Exception as e:
                print(e)

    return render_template("login.html", form=form)


#注册
@main.route('/register', methods=['GET', 'admin'])
def register():
    form = Register()
    if form is None:
        print('shuold input name and password')
    elif form.validate_on_submit():#判断request是个带admin数据，且数据符合表单定义要求
        admin = Admin(id = session.get('id'),
                      name=form.name.data,
                      role_id=form.roleid.data,
                      adminpass=form.adminpass.data
                      )
        # vcode = form.v_code.data
        # if vcode == sms.send_sms()
        db.session.add(admin)
        login_user(admin)
        try:
            #s = requests.Session.admin(url='http://127.0.0.1:5000/login',data=admin.name)
            db.session.commit()
            print('success')
            #print(s)
            #return redirect(url_for("main.index"))
            return redirect(url_for("main.login"))
        except Exception as e:
            db.session.rollback()
            print('failed')
            print(repr(e))
    # if request.method == 'admin':
    #     if form.validate_on_submit():  # 数据正确 并且验证csrf通过
    #         print(request.form.get('userpass'))
    #         print(request.form.get('username'))
    #         return '数据提交成功'
    return render_template("register.html", form=form)

@main.route('/admin')
@login_required
@admin_required
def admin_only():
    return redirect(url_for("main.edit"))

@main.route('/user')
@login_required
@permission_required(Permission.FOLLOW)
def user_only():
    return render_template("user.html")

@main.route('/useradmin')
@login_required
@permission_required(Permission.USERADMIN)
def useradmin_only():
    return "useradmin"

@main.route('/shoperadmin')
@login_required
@permission_required(Permission.SHOPERADMIN)
def shoperadmin_only():
    return "shoperadmin"




