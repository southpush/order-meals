#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 9:46
# @Author  : Min
# @Version : 1.0
import urllib.request, urllib.parse
import datetime
import hashlib
from app.utils.random_mt import random_six


verification_code = random_six()  # 验证码


# MD5加密：
def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


# sid bc3e9587d8694fbb8321cbc15cb56dcb
# token 8b3344f3fb8049a6a7c2ddc37f2b65c0

def send_sms(phone):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    test_data = {'accountSid': 'bc3e9587d8694fbb8321cbc15cb56dcb',
                 'to': phone,
                 'timestamp': timestamp,
                 #'templateid':'1014899612',
                 'smsContent': '【吃货宝】尊敬的用户，您的验证码为%s' % verification_code,
                 'sig': get_md5('bc3e9587d8694fbb8321cbc15cb56dcb' + '8b3344f3fb8049a6a7c2ddc37f2b65c0' + timestamp)
                 }   # ACCOUNT SID + AUTH TOKEN + timestamp

    test_data_urlencode = urllib.parse.urlencode(test_data).encode('utf-8')
    requrl = "https://api.miaodiyun.com/20150822/industrySMS/sendSMS"
    req = urllib.request.Request(url=requrl, data=test_data_urlencode)
    try:
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        return res
    except Exception as e:
        print(repr(e))

#
# if __name__ == '__main__':
#     send_sms()
