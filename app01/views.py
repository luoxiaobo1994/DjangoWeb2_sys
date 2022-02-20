from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Create your views here.

def depart_list(request):
    """  部门列表的处理函数  """
    # 去数据库中获取所有的部门列表,把数据循环放在前端.
    queryset = models.Department.objects.all()  # 得到一个queryset类型,是一个"对象"列表,需要转换.

    return render(request, 'depart_list.html', {"queryset": queryset})


def add_depart(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    title = request.POST.get("title")  # 获取用户输入的数据,数据字段是title,title来源于html里设置的,这个数据的name=title
    models.Department.objects.create(title=title)  # 把数据保存到数据库里.
    return redirect("/depart/list")


def del_depart(request):
    """  删除部门 """
    nid = request.GET.get('nid')  # 获取ID
    models.Department.objects.filter(id=nid).delete()  # 应该按照ID值去删,不能按名称去删.
    # 跳转回部门列表
    return redirect("/depart/list")


def modify_depart(request, nid):  # nid=连接时自带的
    """ 编辑部门 """
    """
    有两种情况会访问这个界面:
    1.从用户列表访问到这个界面.
    2.修改部门名称后,点击提交,也会原地访问这个界面.
    所以,有两种方式的处理,并不冲突.
    """
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的部门信息.
        # nid是直接获取的,不需要再从页面拿了
        row_object = models.Department.objects.filter(id=nid).first()  # 直接拿到那一个真实数据
        return render(request, 'depart_modify.html', {"row_object": row_object})
    # 拿到修改后的部门名称
    new_title = request.POST.get('title')  # 已经在这个界面,进入保存操作,则是POST进来的.
    if new_title:
        models.Department.objects.filter(id=nid).update(title=new_title)
    return redirect("/depart/list/")


def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()
    # depart = models.Department.objects.filter(id=queryset)
    return render(request, 'user_list.html', {'object': queryset})


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
from django import forms


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'create_time', 'gender', 'account', 'depart']
        # widgets = {  # 老土的办法,一个一个去定义,这么写,容易挨叼.
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.PasswordInput(attrs={"class":"form-control"}),
        #     "age":forms.NumberInput(attrs={"class":"form-control"}),
        #     "create_time":forms.TextInput(attrs={"class":"form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name,field)
            field.widget.attrs = {"class": "form-control", "placeholder": name}


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


# ------------------ 靓号管理功能  ----------------------

class PrettyModelForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name,field)
            field.widget.attrs = {"class": "form-control", "placeholder": name}


def pretty_list(request):
    """ 靓号列表 """
    queryset = models.PrettyNum.objects.all().order_by('-level')  # 排序选一个字段,加上-就是倒叙,不加就是升序.
    return render(request, 'pretty_list.html', {'form': queryset})


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


class PrettyEditModelForm(forms.ModelForm):
    # 不让修改手机号
    mobile = forms.CharField(disabled=True,label="手机号")

    class Meta:
        model = models.PrettyNum
        # fields = '__all__'  # 直接引用表里的所有字段
        fields = ['mobile','price', 'level', 'status']  # 自定义需要的字段
        # exclude = ['level'] # 除了被选中的字段,都要.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name,field)
            field.widget.attrs = {"class": "form-control", "placeholder": name}


def pretty_edit(request, nid):
    """ 靓号编辑功能 """
    row_objetc = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyEditModelForm(instance=row_objetc)
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的用户信息.
        return render(request, 'pretty_edit.html', {"form": form})
    # 校验用户数据
    row_objetc = models.UserInfo.objects.filter(id=nid).first()  # 还是拿到要修改的那行数据
    form = PrettyModelForm(data=request.POST, instance=row_objetc)  # instance告诉你要修改这行,不然save就新增数据了.
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})
