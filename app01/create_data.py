# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/6 22:40
# Desc: 往项目的数据库里写一些数据

import random
from faker import Faker
import pymysql

fake = Faker(locale='zh_CN')


def add_user_data(n=10):
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='Lxb@12345',
        database='djangoweb2_sys',
        charset='utf8',
    )
    cursor = db.cursor()
    for i in range(n):
        # 注意写入的字段顺序。很坑。
        info = (
            '0',  # 序号
            fake.name(),  # 姓名
            fake.pystr(),  # 密码
            random.randint(18, 65),  # 年龄
            random.randint(-100000, 10000000),  # 余额
            str(fake.date_between(start_date='-20y', end_date='now')),  # 入职时间
            random.choice(['1', '2']),  # 性别
            random.randint(1, 10)  # 部门
        )
        # print(info)
        sql = f'insert into app01_userinfo values{info};'  # 注意写入的字段顺序。很坑。
        cursor.execute(sql)
    db.commit()
    db.close()
    cursor.close()

def add_phonenum(n=10):
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='Lxb@12345',
        database='djangoweb2_sys',
        charset='utf8',
    )
    cursor = db.cursor()
    for i in range(n):
        # 注意写入的字段顺序。很坑。
        info = (
            '0',  # 序号
            fake.phone_number(), # 电话号码
            random.randint(1,10000),
            random.choice(['1','2','3','4','5']),
            random.choice(['1','2'])
        )
        # print(info)
        sql = f'insert into app01_prettynum values{info};'  # 注意写入的字段顺序。很坑。
        cursor.execute(sql)
    db.commit()
    db.close()
    cursor.close()


if __name__ == '__main__':
    # add_user_data()
    add_phonenum(30)
