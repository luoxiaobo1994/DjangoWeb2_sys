# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/11 14:56
# Desc:

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt  # 免除csrf 校验。
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm


def task_list(request):
    """ 任务列表 """
    return render(request, 'task_list.html')


@csrf_exempt  # 装饰器修饰即可。
def task_ajax(request):
    """ ajax请求的测试函数 """
    # print(request.GET)  # 直接获取到ajax传输的内容。 <QueryDict: {'n1': ['123'], 'n2': ['456']}>

    return HttpResponse("成功收到ajax请求。")
