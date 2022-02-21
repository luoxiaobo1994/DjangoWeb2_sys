# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/21 19:26

""" 自定义的分页组件 :
使用方法:

"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_param="page", page_size=10, plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据(根据这个数据进行分页处理)
        :param page_param: 在URL中传递的获取分页的数据,例如:/pretty/list/?page=12
        :param page_size: 每页显示的数据条数
        :param plus: 分页时,显示当前页的前后多少页
        """
        page = request.GET.get(page_param, '1')  # 当前页
        if page.isdecimal():  # 是否是十进制数
            page = int(page)
        else:
            page = 1  # 不是就给他赋值1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size  # 起始值
        self.end = page * page_size  # 结束值
        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()  # 数据库里的所有数据
        total_page_count, div = divmod(total_count, page_size)  # 求余
        if div:  # 有余数
            total_page_count += 1  # 则+1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出显示当前页的前5页,后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少,都达不到11页
            start_page = 1  # 从第一页开始,避免负数.
            end_page = self.total_page_count  # 到达当前最多的页数.
        else:
            # 数据库中的数据比较多,大于11页
            # 当前页小鱼5页时(极小值).
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页面>5, 且当前页面+5 大于总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        page_str_list = []  # 可选的页面列表.
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))  # 首页标签.
        # 上一页
        if self.page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)
        # 非首页的中间页面
        for i in range(start_page, end_page + 1):  # 顾头不顾尾
            if i == self.page:  # 当前页
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.page + 1)
        else:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(prev)

        # 尾页
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count))
        search_string = """
       <li>
            <form style="float:right;margin-right:10px" method="get">
                <input name="page">
                    style="position:relative;float:left;display:inline-block;width:80px;border-radiu"
            </form>
       
       </li>
        
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
