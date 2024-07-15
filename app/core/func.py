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
    hosts = {
        # 'prod01': '114.116.93.53',
        # 'prod': '114.115.162.96',
        # 'test': '114.116.13.1',
        'elephant': 'elephant',
    }
    for host in hosts:
        if host in url:
            url = url.replace(host, hosts[host])
    if 'http' not in url:
        url = f'http://{url}'
    return url
