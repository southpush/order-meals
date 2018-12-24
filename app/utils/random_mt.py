#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 9:54
# @Author  : Min
# @Version : 1.0
import string, random


def random_six():
    capta = ''

    words = ''.join(string.digits)

    for i in range(6):
        capta += random.choice(words)

    return capta


# verification_code = random_six()   # 验证码
