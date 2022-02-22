# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/22 13:57

import random

from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm
from django import forms

# Create your views here.


def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()
    # depart = models.Department.objects.filter(id=queryset)
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 新增用户(原始的方式):很麻烦,不采取,这是初初初级的程序员才会用的 """
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    # POST请求,先获取用户提交的数据.
    name = request.POST.get("name")
    password = request.POST.get("password")
    gender = request.POST.get("gender")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    department = request.POST.get("department")
    age = request.POST.get("age")
    # 添加到数据库:问题1,没有校验. 问题2,输入错误没有提示. 问题3,输入错误,跳转报错界面,不美观. 问题4,每个字段都重新校验则比较麻烦.
    models.UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        gender=gender,
        account=float('%.2f' % account),  # 取两位小数
        create_time=create_time,
        depart_id=department
    )
    return redirect("/user/list/")


# --------------- ModelForm实例 ---------------



def user_add_model(request):
    """ 新增用户 使用模板表单ModelForm,使用组件,把一些校验操作,提示操作完成了. """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})
    # 获取POST提交的数据,并对数据进行校验.
    form = UserModelForm(data=request.POST)
    if form.is_valid():  # 校验成功.
        # print(form.cleaned_data)
        form.save()  # 直接保存到数据库里,简直不要太粗暴...
        return redirect("/user/list")
    # 校验失败.在页面上显示错误信息.
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    row_objetc = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(instance=row_objetc)
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的用户信息.
        return render(request, 'user_edit.html', {"form": form})
    # 校验用户数据
    row_objetc = models.UserInfo.objects.filter(id=nid).first()  # 还是拿到要修改的那行数据
    form = UserModelForm(data=request.POST, instance=row_objetc)  # instance告诉你要修改这行,不然save就新增数据了.
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
