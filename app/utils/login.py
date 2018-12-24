#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 16:24
# @Author  : Min
# @Version : 1.0
from functools import wraps
from flask_login import current_user
from ..utils.response import general_response
from app.models.admin import Permission


# 权限装饰器
def permission_required(permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # print(permissions)
            count = 0
            # 遍历permissions,如果有该权限 count+1
            for i in permissions:
                # print(i)
                if current_user.can(i):
                    # print(current_user.can(i))
                    count += 1
            # count为零返回403
            if count == 0:
                return general_response(err_code=2003)
            return f(*args, **kwargs)

        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


