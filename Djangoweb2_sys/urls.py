"""Djangoweb2_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import user, depart, pretty_number, admin

urlpatterns = [
    path('', user.user_list),  # '' 表示在http://127.0.0.1:8000后面,什么都不加了.就是把默认的主页指向后面的这个函数里.
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.add_depart),
    path('depart/delete/', depart.del_depart),
    # 带有正则筛选功能的连接地址,访问时,必须传入一个数值.eg:depart/2/modify/,depart/1/modify/
    # 使用这种方式,view函数可以多传一个nid参数.
    path('depart/<int:nid>/modify/', depart.modify_depart),
    # 下面是关于用户的函数
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model_add/', user.user_add_model),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),
    # 下面是关于靓号管理的.
    path('pretty/list/', pretty_number.pretty_list),
    path('pretty/add/', pretty_number.pretty_add),
    path('pretty/<int:nid>/edit/', pretty_number.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty_number.pretty_delete),
    # 下面是管理员管理相关功能
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

]
