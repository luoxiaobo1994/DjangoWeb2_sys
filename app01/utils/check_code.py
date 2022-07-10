# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/10 17:03
# Desc: 用于生成随机验证码的图片.

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def check_code(width=120, height=30, char_lengrh=5, font_file='app01/static/font/agua-regular1.0.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw(img, mode='RGB')


    def rndChar():
        """ 生成随机字母 """
        return chr(random.randint(65, 90))

    def rndColor():
        """ 生成随机颜色 """
        return (random.randint(0,255),random.randint(10,255),random.randint(64,255),)


