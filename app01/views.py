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
