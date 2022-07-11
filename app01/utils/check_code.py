# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/10 17:03
# Desc: 用于生成随机验证码的图片.

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

fontfile = 'app01/static/font/simhei.ttf'


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
    for i in range(30):  # 调少一点，太多了。
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
    # 写干扰圆圈
    for i in range(30):  # 调少一点，太多了。
        draw.point((random.randint(0, width), random.randint(0, height)), fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(3):  # 调少一点，太多了。
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


if __name__ == '__main__':
    img, code = check_code()
    # with open('code_demo.png', 'wb') as f:
    #     img.save(f, format='png')  # 需要保存,图片才生效.
    print(code)
