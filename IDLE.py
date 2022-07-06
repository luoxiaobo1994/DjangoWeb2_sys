# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/5 20:00
# Desc: 调试平台

import requests

res = requests.get(url="http://127.0.0.1:8000/app01/getuser?nid=1")
print(res.json())

