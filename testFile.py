# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
def login_required(parser):
    def decorator(func):
        def wrapper(*args, **kw):
            if parser == 1:
                print(parser)
                return False
            else:
                print(parser)
            return func(*args, **kw)
        return wrapper
    return decorator


@login_required(1)
def test():
    print("you are in the test")


if __name__ == '__main__':
    url = "https://wx.qlogo.cn/mmopen/vi_32/Y9mCvSdYhRNicK2ib0C7Bdv1oPOyCHQHb7IV6IchryJ2gtdQoNO2aB8eNan2IyfYJRKw7hsQ0UoTleicXic5a2ddgg/132"
    r = requests.get(url).content
    print(r)
