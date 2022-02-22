# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/22 13:57

import random
from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.pagination import Pagination
from django.forms import forms
from app01.utils.form import PrettyModelForm,PrettyEditModelForm


# Create your views here.



def add_phone_number(n):
    for i in range(n):
        models.PrettyNum.objects.create(
            mobile=str(random.choice([13, 15, 17, 18, 19])) + str(random.randint(100000000, 999999999)),
            price=random.randint(0, 1000),
            level=random.randint(1, 5),
            status=random.randint(1, 2))


def pretty_list(request):
    """ 靓号列表 """
    # 补充查询功能. 不再函数功能里,只是知识补充.
    # 判断条件字段是数值型的,例如主键,大于小于等于的判断.
    # models.PrettyNum.objects.all().filter(id=12)  # 查询id=12的那行数据,得到的queryset对象列表.
    # models.PrettyNum.objects.all().filter(id__gt=12)  # 大于12
    # models.PrettyNum.objects.all().filter(id__gte=12)  # 大于等于12
    # models.PrettyNum.objects.all().filter(id__lt=12)  # 小于12
    # models.PrettyNum.objects.all().filter(id__lte=12)  # 小于等于12
    # 判断条件是字符串的,例如本例的手机号码.
    # xx = models.PrettyNum.objects.all().filter(mobile__startswith='13')
    # xx = models.PrettyNum.objects.all().filter(mobile__endswith='30')
    # xx = models.PrettyNum.objects.all().filter(mobile__contains='30')
    # xx = models.PrettyNum.objects.all().filter(mobile__isnull=True)
    # add_phone_number(100) # 快速生成数据.  简直不要太快.
    # models.PrettyNum.objects.filter(id__gte=206).delete()  # 快速删除

    data_dict = {}  # 筛选条件的字典.
    # # 获取get请求的参数值.
    search_data = request.GET.get('q', "")
    # print(f"search_data:{search_data},type:{type(search_data)}")
    if search_data:
        data_dict['mobile__contains'] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('id')  # 排序选一个字段,加上-就是倒叙,不加就是升序.
    page_object = Pagination(request=request, queryset=queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """ 靓号添加功能 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request, 'pretty_add.html', {"form": form})





def pretty_edit(request, nid):
    """ 靓号编辑功能 """
    row_objetc = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的用户信息.
        form = PrettyEditModelForm(instance=row_objetc)
        return render(request, 'pretty_edit.html', {"form": form})
    # 校验用户数据
    form = PrettyEditModelForm(data=request.POST, instance=row_objetc)  # instance告诉你要修改这行,不然save就新增数据了.
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """ 靓号删除功能 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
