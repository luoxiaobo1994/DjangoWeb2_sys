# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/6 14:30
# Desc: 接口函数。

import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from app01 import models
from app01.views.user import UserModelForm


def user_token(request):
    obj = json.loads(request.body)
    # 1.先获取到接口传入的参数。
    username = obj.get('username', None)
    password = obj.get('password', None)

    if all([username, password]):  # 全部都填入了。
        row_object = models.Admin.objects.filter(username=username, password=password)
        is_login = authenticate(request, username=username, password=password)
        data = model_to_dict(row_object)  # 转成字典
        if data:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(is_login)
            token = jwt_encode_handler(payload)
            print(f"token:{token}")
            print(f"在数据库中查询到的结果：{data},生成的Token:{token}")
            return JsonResponse({'code': 200, 'msg': 'request succeeded', 'token': token})
        return JsonResponse({'code': 403, 'msg': 'bad request: Incorrect username or password'})

    else:
        return JsonResponse({'code': 403, 'msg': 'bad request: Account and password cannot be empty'})


def get_user(request):
    if request.method == "GET":
        # queryset = models.UserInfo.objects.all()  # 这是查询所有的，接口的目的肯定是查指定的，暂时不能这么查。
        nid = request.GET.get('nid')
        # nid = 1
        if nid:
            row_object = models.UserInfo.objects.filter(id=nid).first()  # 获取当行数据
            data = model_to_dict(row_object)  # 把行数据(表单信息)转换为字典。
            print(f"结果：------------------------------------------：{data}")
            return JsonResponse({'code': 100200, 'msg': '查询成功。', 'data': data})  #
        else:
            return JsonResponse({'code': 100101, 'msg': "查询失败，请输入正确的用户id。"})
    else:
        return JsonResponse({'code': 100102, 'msg': "请求方法错误，请检查。"})


def add_user(request):
    if request.method == "POST":
        print(f"request.Post data:[{request.POST}]")
        # print(f"---> {model_to_dict(request.POST)}")
        form = UserModelForm(data=request.POST)  # 理论上应该是可以的，但是不行。
        # print(f"----->{form.data}")  # 这个可以把数据弄出来。
        if form.is_valid():
            form.save()  # 合法就保存。
            return JsonResponse({'code': 100200, 'msg': '新增用户成功。'})
        else:
            # error_data = model_to_dict(form)  # 不行
            # print(f"---->{form.errors}")  # 不行
            return JsonResponse({'code': 100101, 'msg': '新增用户数据失败，请检查数据准确性。'})
    else:
        return JsonResponse({'code': 100102, 'msg': "请求方法错误，请检查。"})


def edit_user(request, nid):
    if request.method == "POST":
        # nid = request.POST.get('nid')
        if nid:
            row_object = models.UserInfo.objects.filter(id=nid).first()  # 第一次拿。
            if row_object:  # 存在于数据库里
                before_data = model_to_dict(row_object)
                print(f"request.Post data:[{request.POST}]")
                row_object = models.UserInfo.objects.filter(id=nid).first()  # 不知道为什么，修改之前，还得再拿一次。
                form = UserModelForm(data=request.POST, instance=row_object)
                if form.is_valid():  # 数据合法
                    form.save()  # 先保存
                    after_data = model_to_dict(models.UserInfo.objects.filter(id=nid).first())  # 再获取，才是对的。
                    return JsonResponse(
                        {'code': 100200, 'msg': "修改成功。", 'before_data': before_data, 'after_data': after_data})
                else:  # 数据不合法
                    return JsonResponse({'code': 100202, 'msg': '修改失败，请检查数据准确性。'})
            else:  # 指定id在数据库查不到数据。
                return JsonResponse({'code': 100201, 'msg': "输入的id，对应用户不存在，修改操作无效。"})
        else:  # 没有填参数
            return JsonResponse({'code': 100101, 'msg': "数据错误：用户id是必要参数。"})
    else:
        return JsonResponse({'code': 100102, 'msg': "请求方法错误，请检查。"})


def del_user(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        if nid:
            row_object = models.UserInfo.objects.filter(id=nid).first()  # 获取当行数据
            if row_object:
                user_data = model_to_dict(row_object)  # 数据转换为可显示字典
                models.UserInfo.objects.filter(id=nid).delete()  # 删掉。
                # user_data = model_to_dict(user_data)
                return JsonResponse({'code': 100200, 'msg': "删除用户成功。", 'data': user_data})
            else:
                return JsonResponse({'code': 100201, 'msg': "数据库中已无此用户。删除操作无效。"})
        else:
            return JsonResponse({'code': 100101, 'msg': "数据错误：用户id是必要参数。"})
    else:
        return JsonResponse({'code': 100102, 'msg': "请求方法错误，请检查。"})
