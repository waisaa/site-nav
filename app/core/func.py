import os
from core.const import Const


def get_new_img_id():
    """获取新图片的序号"""
    res = 0
    for img in os.listdir(Const.DIR_BG):
        bgid = int(img[2:3])
        if bgid > res:
            res = bgid
    return res + 1


def fmt_url(url):
    """格式化url"""
    return url if 'http' in url else f'http://{url}'
