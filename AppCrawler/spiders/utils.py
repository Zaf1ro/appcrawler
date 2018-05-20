# !/usr/bin/python
# coding: utf-8

import time
from collections import OrderedDict
# from ..utils.category import *


# 时间统计
def get_current_time():
    now = int(time.time())
    return now, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))


def get_interval_time(t1, t2):
    return abs(t2 - t1)


def handle_category(cat, store):
    if type(cat) != int:
        print("error")
        return None

    if store == 'baidu':
        categories = CATEGORY_baidu
    elif store == 'tencent':
        categories = CATEGORY_tencent
    else:
        categories = CATEGORY_360

    if cat >= len(categories) or cat < 0:
        print("error")
        return None
    elif cat:
        return [categories[cat]]
    else:
        return categories
