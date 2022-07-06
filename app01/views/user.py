# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/22 13:57

from django.shortcuts import render, redirect
from django.http import JsonResponse
from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


# Create your views here.


def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()  # 数据库里的所有数据。
    # depart = models.Department.objects.filter(id=queryset)
    page_object = Pagination(request, queryset, page_size=10)  # 分页工具
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户功能 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_add.html', {'form': form})


# --------------- ModelForm实例 ---------------


def user_add_model(request):
    """ 新增用户 使用模板表单ModelForm,使用组件,把一些校验操作,提示操作完成了. """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})
    # 获取POST提交的数据,并对数据进行校验.
    form = UserModelForm(data=request.POST)
    print(f"request.Post:{request.POST}")
    if form.is_valid():  # 校验成功.
        print(f"form_cleaned_data:{form.cleaned_data}")
        form.save()  # 直接保存到数据库里,简直不要太粗暴...
        return redirect("/user/list")
    # 校验失败.在页面上显示错误信息.
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(instance=row_object)
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的用户信息.
        return render(request, 'user_edit.html', {"form": form})
    # 校验用户数据
    row_object = models.UserInfo.objects.filter(id=nid).first()  # 还是拿到要修改的那行数据
    form = UserModelForm(data=request.POST, instance=row_object)  # instance告诉你要修改这行,不然save就新增数据了.
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def user_listapi(request, nid):
    return JsonResponse({'status': 200})

# def user_
