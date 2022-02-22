# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/22 14:01

from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm



# 编辑的单独ModelForm类,因为编辑和新建的校验规则不一样,所以新建一个更好.
class PrettyEditModelForm(BootStrapModelForm):
    # 不让修改手机号
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        # fields = '__all__'  # 直接引用表里的所有字段
        fields = ['mobile', 'price', 'level', 'status']  # 自定义需要的字段
        # exclude = ['level'] # 除了被选中的字段,都要.


    # 校验手机号
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(
            mobile=txt_mobile).exists()  # 校验,这个数据是否存在于数据库中
        if exists:  # 返回的是bool值
            raise ValidationError("手机号已存在")
        # elif len(txt_mobile) != 11:
        #     raise ValidationError('手机号长度不正确')
        return txt_mobile


# ------------------ 靓号管理功能  ----------------------

class PrettyModelForm(BootStrapModelForm):
    # 验证的方式1,直接找指定字段,添加校验规则.
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^1[3-9]\d{9}$", '手机号格式错误')]
    )

    # 校验的方式2,钩子方法. 无需调用,直接生效.  前提是要有这个字段.
    # def clean_mobile(self):
    #     text_mobile = self.cleaned_data['mobile']
    #     if len(text_mobile) != 11:
    #         # 验证不通过,把错误原因返回.
    #         raise ValidationError("格式错误:长度不足11位.")
    #     # 验证通过,把用户输入的值返回
    #     return text_mobile

    class Meta:
        model = models.PrettyNum
        # fields = '__all__'  # 直接引用表里的所有字段
        fields = ['mobile', 'price', 'level', 'status']  # 自定义需要的字段
        # exclude = ['level'] # 除了被选中的字段,都要.



class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'create_time', 'gender', 'account', 'depart']
        # widgets = {  # 老土的办法,一个一个去定义,这么写,容易挨叼.
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.PasswordInput(attrs={"class":"form-control"}),
        #     "age":forms.NumberInput(attrs={"class":"form-control"}),
        #     "create_time":forms.TextInput(attrs={"class":"form-control"}),
        # }