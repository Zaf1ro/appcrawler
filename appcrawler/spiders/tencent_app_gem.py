# !/usr/bin/python
# coding: utf-8

import json
from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from ..items import TencentAppGemItem

# Limit of APP number of each category
MAX_APP = 100

# Category
CATEGORY = {
    '100': 0,
    '101': 0,
    '102': 0,
    '103': 0,
    '104': 0,
    '105': 0,
    '106': 0,
    '107': 0,
    '108': 0,
    '109': 0,
    '110': 0,
    '111': 0,
    '112': 0,
    '113': 0,
    '114': 0,
    '115': 0,
    '116': 0,
    '117': 0,
    '118': 0,
    '119': 0,
    '122': 0
}

DOMAIN = 'http://android.app.qq.com'
CATEGORY_URL = 'http://android.app.qq.com/myapp/cate/appList.htm?categoryId='
EXTENDED_URL = '&pageSize=20&pageContext='


class AppSpider(Spider):
    name = "tencent"

    def __init__(self, *args, **kwargs):
        super(AppSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["qq.com"]
        # self.categories = handle_category(cat, 'tencent')
        # self.save - 保存方式 - unfinished

    def start_requests(self):
        for category_code in CATEGORY.keys():
            yield Request(
                url=CATEGORY_URL + category_code + EXTENDED_URL + '0',
                callback=self.parse,
                meta={
                    'category_code': category_code,
                    'start': 20
                }
            )

    def parse(self, response):
        if response.status != 200:
            raise CloseSpider('Error with network')

        json_data = json.loads(response.body_as_unicode())
        category_code = response.meta['category_code']
        total_count = json_data['count']
        stop_flag = total_count < 20 or CATEGORY[category_code] >= MAX_APP

        for app_info in json_data['obj']:
            self.parse_app(app_info)
        CATEGORY_URL[category_code] += total_count

        if not stop_flag:
            start = response.meta['start']
            yield Request(
                url=CATEGORY_URL + category_code + EXTENDED_URL + start,
                callback=self.parse,
                meta={
                    'category_code': category_code,
                    'start': start+20
                }
            )

    @staticmethod
    def parse_app(app_info):
        app_item = TencentAppGemItem()
        app_item['app_name'] = app_info['appName']
        app_item['apk_size'] = app_info['fileSize']
        app_item['apk_url'] = app_info['apkUrl']
        app_item['download_count'] = app_info['appDownCount']
        app_item['seller'] = app_info['authorName']
        app_item['rating'] = app_info['averageRating']
        app_item['category'] = app_info['categoryName']
