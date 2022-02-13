from django.shortcuts import render, redirect
from app01 import models


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
    form = UserModelForm()
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    user_info = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":  # 从用户列表访问这个界面. 则显示你要修改的部门信息.
        return render(request, 'user_edit.html', {"user_info": user_info})
    # 拿到修改后的部门名称
    new_title = request.POST.get('title')  # 已经在这个界面,进入保存操作,则是POST进来的.
    if new_title:
        models.Department.objects.filter().update(title=new_title)
    return redirect("/user/list/")
