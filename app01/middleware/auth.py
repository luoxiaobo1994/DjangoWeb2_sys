# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/7 23:42
# Desc: 用来做鉴权的中间件。在这里做鉴权即可，不用在每个页面单独做。

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from time import sleep
from app01.views.account import LoginForm


class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 如果中间件没有返回值（None），则继续往后走。
        # print("中间件M1.进来了。")
        # 如果有返回值。则可以返回HttpResponse,JsonResponse,以及重定向。
        # ---------
        # 排除一些不需要鉴权的url
        if request.path_info == '/login':
            return  # 登录页面无需鉴权，直接进。
        info = request.session.get("info")
        # print(f"user session：{info}。")
        if not info:  # 没有登录信息
            form = LoginForm()  # 不需要数据。只是给页面调整一下表单样式。
            # form.add_error("username", "请先登录。")  # 后面也许可以做一个弹窗提示，更好些。
            return render(request, 'login.html', {'form': form})  # 页面有点问题。需要form表单。
        else:
            return render(request, 'user_list.html')
        # return JsonResponse({'code': 404, 'msg': "无权访问。"})

    def process_response(self, request, response):
        # print("中间件M1.出去了。")
        return response

# class M2(MiddlewareMixin):
#     """ 中间件1 """
#
#     def process_request(self, request):
#         print("中间件M2.进来了。")
#
#     def process_response(self, request, response):
#         print("中间件M2.出去了。")
#         return response
#
#
# class M3(MiddlewareMixin):
#     """ 中间件1 """
#
#     def process_request(self, request):
#         print("中间件M3.进来了。")
#
#     def process_response(self, request, response):
#         print("中间件M3.出去了。")
#         return response
