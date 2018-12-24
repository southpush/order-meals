# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 16:48
# @Author  : Min
# @Version : 1.0
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length,Required


class Login(FlaskForm): # 继承自FlaskForm类

    name = StringField('用户名', validators=[Length(min=3,max=12,message='用户名长度为3~12位'),DataRequired(message='用户名不能为空')], description="用户名")
    adminpass = PasswordField('密码',validators=[Length(min=6,max=12,message='密码长度为6~12位'),DataRequired(message='密码不能为空')], description="密码")
    roleid = SelectField('角色', coerce=int, validators=[DataRequired("请选择角色")], choices=[(1,"用户"), (2,"商铺管理员"), (3,"用户管理员"),(4,"超级管理员")], description="选择角色")
    login = SubmitField('login')
    logout = SubmitField('logout')


class Register(FlaskForm): # 继承自FlaskForm类

    name = StringField('用户名', validators=[Length(min=3,max=12,message='用户名长度为3~12位'),DataRequired(message='用户名不能为空')], description="用户名")
    adminpass = PasswordField('密码',validators=[Length(min=6,max=12,message='密码长度为6~12位'),DataRequired(message='密码不能为空')], description="密码")
    roleid = SelectField('角色', coerce=int, validators=[DataRequired("请选择角色")], choices=[(1,"用户"), (2,"商铺管理员"), (3,"用户管理员"),(4,"超级管理员")], description="选择角色")
    #rolepermission = SelectField('角色', coerce=int, validators=[DataRequired("请选择角色")], choices=[(1,"用户"), (2,"商铺管理员"), (4,"用户管理员"),(0,"超级管理员")], description="选择角色")

    register = SubmitField('register')


class Edit(FlaskForm): # 继承自FlaskForm类

    name = StringField('用户名')
    adminpass = PasswordField('密码', validators=[DataRequired()])
    newpass = PasswordField('新密码', validators=[DataRequired()])
    #adminphone = StringField('手机号码', validators=[Length(min=8,max=11,message='手机号码长度为8~11位'), DataRequired(message='手机号码不能为空')])
    submit = SubmitField('修改')


class Phone(FlaskForm):
    phone = StringField('手机号码', validators=[DataRequired()])
    v_code = StringField('验证码')
    send = SubmitField('获取短信验证码')
