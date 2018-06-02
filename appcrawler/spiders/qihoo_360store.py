# !/usr/bin/python
# coding: utf-8

import logging
import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from ..items import QihooItem

# Limit of pages
MAX_APPS_PER_PAGE = 2

# Category
CATEGORY = {
    'security': 'http://zhushou.360.cn/list/index/cid/11',
    'social': 'http://zhushou.360.cn/list/index/cid/12',
    'video': 'http://zhushou.360.cn/list/index/cid/14',
    'news': 'http://zhushou.360.cn/list/index/cid/15',
    'lifestyle': 'http://zhushou.360.cn/list/index/cid/16',
    'wallpaper': 'http://zhushou.360.cn/list/index/cid/18',
    'business': 'http://zhushou.360.cn/list/index/cid/17',
    'photo': 'http://zhushou.360.cn/list/index/cid/102228',
    'travel': 'http://zhushou.360.cn/list/index/cid/102231',
    'education': 'http://zhushou.360.cn/list/index/cid/102232',
    'finance': 'http://zhushou.360.cn/list/index/cid/102139',
    'health': 'http://zhushou.360.cn/list/index/cid/102233',
}

# URL
DOMAIN = "http://zhushou.360.cn"
# CATEGORY_URL = "http://zhushou.360.cn/list/index/cid/"
# ORDER_BY_DOWNLOAD_URL = "/order/download/?page="
# APP_URL = "http://zhushou.360.cn/detail/index/soft_id/"

# XPATH
XPATH_APP_URL = "//*[@id='iconList']/li/h3/a/@href"  # OK
XPATH_DOWNLOAD_URL = "//*[@id='app-info-panel']/div/dl/dd/a/@href"  # OK
XPATH_DOWNLOAD_TIMES = "//*[@id='app-info-panel']/div/dl/dd/div/span[3]/text()"  # OK
XPATH_APP_NAME = "//*[@id='app-name']/span/@title"  # OK
XPATH_APP_RATING = "//div[@class='pf']/span[1]/text()"
XPATH_APP_SIZE = "//div[@class='pf']/span[4]/text()"


class QihooSpider(scrapy.Spider):
    name = "qihoo"
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    def __init__(self, *args, **kwargs):
        super(QihooSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["360.cn"]
        # self.cat = cat
        # self.cats, self.reverse_id = self.handle_cat(cat)
        # print(self.cats)
        # print(self.reverse_id)
        # self.fail_log = open("log.txt", "w+")

    # start with category urls
    def start_requests(self):
        name = 'security'
        category_url = 'http://zhushou.360.cn/list/index/cid/11'
        # for name, category_url in CATEGORY.items():
        yield Request(
            url=category_url,
            callback=self.parse,
            meta={'category_name': name}
        )

    # category -> page number
    def parse(self, response):
        if response.status != 200:
            CloseSpider('Error with network')

        category_name = response.meta['category_name']
        for i in range(1, MAX_APPS_PER_PAGE):

            file = open('testfile.txt', 'w')
            file.write(category_name)
            file.close()

            yield Request(
                url=response.url + '?page=%d' % i,
                callback=self.parse_page,
                meta={
                    'category_name': category_name,
                    'page': i
                }
            )

    # page number -> app page
    def parse_page(self, response):
        app_urls = response.xpath(XPATH_APP_URL).extract()
        for url in app_urls[0:1]:
            yield Request(
                url=DOMAIN + url,
                callback=self.parse_app,
                meta={
                    'category_name': response.meta['category_name'],
                    'page': response.meta['page']
                }
            )

    def parse_app(self, response):
        app_item = QihooItem()
        app_item['category'] = response.meta['category_name']
        app_item['name'] = response.xpath(XPATH_APP_NAME).extract()[0]
        app_item['rating'] = response.xpath(XPATH_APP_RATING).extract()[0]  # 7.6分
        app_item['apk_url'] = response.xpath(XPATH_DOWNLOAD_URL).extract()[0]
        raw_download_times = response.xpath(XPATH_DOWNLOAD_TIMES).extract()[0]
        app_item['download_count'] = raw_download_times.spilt(': ')[1]
        app_item['apk_size'] = response.xpath(XPATH_APP_SIZE).extract()[0]

        yield app_item

