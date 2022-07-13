# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/11 14:56
# Desc:

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt  # 免除csrf 校验。
from django import forms
from app01 import models
from app01.utils.form import BootStrapModelForm
from django.http import JsonResponse
import json


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"  # 自动填充所有字段。
        widgets = {
            'detail': forms.TextInput  # 普通的输入框.
            # 'detail': forms.Textarea  # 巨大输入框. 更方便任务描述. 但是排版一般.
        }


def task_list(request):
    """ 任务列表 """
    form = TaskModelForm()
    return render(request, 'task_list.html', {'form': form})


@csrf_exempt  # 装饰器修饰即可。
def task_ajax(request):
    """ ajax请求的测试函数 """
    # print(request.GET)  # 直接获取到ajax传输的内容。 <QueryDict: {'n1': ['123'], 'n2': ['456']}>

    return HttpResponse("成功收到ajax请求。")


@csrf_exempt  # 装饰器修饰即可。
def task_add(request):
    """ 新增任务 """
    print(f"post data:{request.POST}")
    # 用户发送过来的数据进行校验.
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'result': True})
    # print(f"form.errors : {form.errors} ------------")  # type:django.forms.utils.ErrorDict
    data_dict = {'result': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 错误类型转字典.
