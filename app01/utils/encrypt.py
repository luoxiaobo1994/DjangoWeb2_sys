# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/22 23:11

import hashlib
from django.conf import settings


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

print(md5('lxb'))