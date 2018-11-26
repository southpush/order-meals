# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
    s = Serializer('123456', expires_in=7200)
    token = s.dumps({"id": 8}).decode("ascii")
    sa = Serializer("123456")
    data = sa.loads(token)
    print(token)
    print(sa.loads(token))
