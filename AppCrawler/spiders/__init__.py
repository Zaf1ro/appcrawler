# !/usr/bin/python
# coding: utf-8

import time
from collections import OrderedDict


# 360_TYPE_ID
TYPE_ID = OrderedDict([
    ("safe", [11, u"系统安全"]),
    ("im", [12, u"通讯社交"]),
    ("audio", [14, u"影音视听"]),
    ("news", [15, u"新闻阅读"]),
    ("life", [16, u"生活休闲"]),
    ("pic", [18, u"主题壁纸"]),
    ("biz", [17, u"办公商务"]),
    ("cam", [102228, u"摄影摄像"]),
    ("map", [102231, u"地图旅游"]),
    ("edu", [102232, u"教育学习"]),
    ("fin", [102139, u"金融理财"]),
    ("fit", [102233, u"健康医疗"])
])


# 时间统计
def get_current_time():
    now = int(time.time())
    return now, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))


def get_interval_time(t1, t2):
    return abs(t2 - t1)
