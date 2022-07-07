# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/7 14:26
# Desc:

from django.shortcuts import render
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm


class LoginForm(BootStrapForm):
    # 自定义的字段，用于校验用户数据，一般的Form表单。
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)  # 必填，但是校验也会做，以及默认是开
    password = forms.CharField(label="密码", widget=forms.PasswordInput)  # 所以必填可以省略。


class LoginModelForm(forms.ModelForm):
    # 使用modelForm实现,本次使用Form实现，暂不用这个。
    class Meta:
        model = models.Admin
        fields = ['username', 'password']


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功。
        print(form.cleaned_data)
        # form.save() # 这个操作是不存在的。这里没有数据连接，和存储操作。Form类也没有对接的数据库。
        return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'error_page.html', {'error_msg': "账户验证失败，登陆操作不成功。", 'error_title': "登陆失败"})

    # else:
    #     return render(request, 'error_page.html', {'m'})
