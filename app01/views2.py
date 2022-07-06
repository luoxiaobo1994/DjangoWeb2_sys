# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/6 14:30
# Desc:

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from app01 import models
from app01.utils.form import UserModelForm
from django.forms.models import model_to_dict


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
    return JsonResponse({'status': 200})
