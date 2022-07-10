# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/7 14:26
# Desc:

import random
from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

fontfile = '../static/font/agua.ttf'


class LoginForm(BootStrapForm):
    # 自定义的字段，用于校验用户数据，一般的Form表单。
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)  # 必填，但是校验也会做，以及默认是开
    # render_value = Ture, 填写错误的情况下。错误的密码仍然保留。
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))  # 所以必填可以省略。

    def clean_password(self):  # 定义一个钩子函数。校验密码
        password = self.cleaned_data.get('password')
        return md5(password)


# class LoginModelForm(forms.ModelForm):
#     # 使用modelForm实现,本次使用Form实现，暂不用这个。
#     class Meta:
#         model = models.Admin
#         fields = ['username', 'password']
#     # 不用这个，别加函数在这。


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功。
        # {'username': '1231241', 'password': '659864b5b65cc0141141eacbd246a421'} # 返回md5的情况。数据库里存的是md5。
        print(form.cleaned_data)  # 后台日志：{'username': '17503056030', 'password': 'asddaa'}，直接返回的是字典。
        # form.save() # 这个操作是不存在的。这里没有数据连接，和存储操作。Form类也没有对接的数据库。
        # 去数据库脚丫用户名和密码是否正确。
        # models.Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()  # 字典解包，直接对上上面的查询条件。
        if not admin_object:  # 有数据是错误的
            form.add_error("password", "用户名或密码错误")  # 校验失败时，在密码下面显示错误信息。
            return render(request, 'login.html', {'form': form})
        # 账户密码正确的情况下。
        # 网站生成随机字符串，作为cookie写在用户本地浏览器中。再写到session里。
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}  # 一步到位，直接生成了。按用户名生成。
        # print(request.session)
        return redirect('/admin/list/')  # 重定向时不需要传request参数。
    form.add_error("username", "请求错误。")  # 有点多余，网页上不会这样，接口的话，这个也返回不了什么的样子。
    return render(request, 'login.html', {'form': form})
    # else:  # 本页面直接提示即可，不用跳错误页面了。 更直观。
    #     return render(request, 'error_page.html', {'error_msg': "账户验证失败，登陆操作不成功。", 'error_title': "登陆失败"})


def image_code(request):
    """ 生成随机验证码 """

    # 调用
    img, code_str = check_code(font_file=fontfile)
    print(code_str)
    # return JsonResponse({'code': '200', 'msg': code})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')




def check_code(width=120, height=30, char_lengrh=5, font_file=fontfile, font_size=28):
    """ 返回一个图像对象和图像的文本内容 """
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """ 生成随机字母 """
        return chr(random.randint(65, 90))

    def rndColor():
        """ 生成随机颜色 """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255),)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_lengrh):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_lengrh + 0.1, h + 0.1], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
    # 写干扰圆圈
    for i in range(40):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
