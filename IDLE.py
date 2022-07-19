# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/5 20:00
# Desc: 调试平台

import requests


def getuser_api():
    res = requests.get(url="http://127.0.0.1:8000/app01/getuser?nid=1")
    print(res.json())


def adduser_api():
    data = {
        # 'csrfmiddlewaretoken': 'cjW9Q4xZDAQWKnSphn1UQtJJF7PWm1lp1dj8lrPRd1RYlTcNvAKzda3CvxMmUFHv',
        'name': 'api_test01',
        'password': "apiapi",
        'age': '25',
        'create_time': '2022-07-15',
        'gender': '1',  # 大坑，性别是枚举类型。
        'account': '100.2',
        'depart': '2'  # 部门也是枚举类型。干
    }
    res = requests.post(url='http://127.0.0.1:8000/app01/adduser', data=data)
    print(res.json())


def edituser_api(nid):
    data = {
        # 'csrfmiddlewaretoken': 'cjW9Q4xZDAQWKnSphn1UQtJJF7PWm1lp1dj8lrPRd1RYlTcNvAKzda3CvxMmUFHv',
        'name': 'api_test044',
        'password': "xxxxapiapi",
        'age': '28',
        'create_time': '2022-06-30',
        'gender': '2',  # 大坑，性别是枚举类型。
        'account': '3012.2',
        'depart': '3'  # 部门也是枚举类型。干

    }
    res = requests.post(url='http://127.0.0.1:8000/app01/edituser/{}/'.format(nid), data=data)
    print(res.json())


def deluser_api():
    data = {
        'nid': 11
    }
    res = requests.post(url='http://127.0.0.1:8000/app01/deluser', data=data)
    print(res.json())


def get_token():
    data = {
        'username': 'luoxiaobo',
        'password': 'lxb@12345'
    }
    res = requests.get(url='http://127.0.0.1:8000/app01/gettoken', data=data)
    print(res.json())

if __name__ == '__main__':
    # adduser_api()
    # deluser_api()
    # edituser_api(17)
    get_token()