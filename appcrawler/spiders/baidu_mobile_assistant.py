# !/usr/bin/python
# coding: utf-8

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from ..items import BaiduMobileAssistantItem


# Category
CATEGORY = [
    [501, u"系统工具"],
    [502, u"主题壁纸"],
    [503, u"社交通讯"],
    [508, u"拍摄美化"],
    [506, u"影音播放"],
    [504, u"生活实用"],
    [510, u"理财购物"],
    [507, u"办公学习"],
    [505, u"咨询阅读"],
    [509, u"旅游出行"]
]

# URL
Domain = "http://shouji.baidu.com"
CATEGORY_URL = "http://shouji.baidu.com/software/"

# XPATH
XAPTH_APP_NAME = ''


class MAINSpider(Spider):
    name = "baidu"

    def __init__(self, cat=None, save=None, *args, **kwargs):
        super(MAINSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["baidu.com"]
        self.categories = handle_category(cat, 'baidu')
        # self.save - 保存方式 - unfinished

        self.start_urls = [
            Domain,
        ]

    def parse(self, response):
        # 网络情况
        if response.status != 200:
            raise CloseSpider(u"网络状况有问题.")

        for pair in self.categories:
            t1, printable_time = get_current_time()
            print(printable_time + " : Start to crawl " + pair[1])

            for i in range(1, 2):  # 页数
                yield Request(url=CATEGORY_URL + str(pair[0]) + '&page_num=' + str(i), callback=self.parse_page)

            t2, printable_time = get_current_time()
            print(printable_time + " : End to crawl " + pair[1] + " taking %d s" % (get_interval_time(t1, t2)))

    def parse_single_category(self, response):
        app_urls = response.xpath(APP_URL_XPATH)
        for url in app_urls:
            yield Request(url=Domain + url, callback=self.parse_single_app)

    @staticmethod
    def parse_single_app(response):
        item = Item_tencent()
        item['name'] = response.xpath(XPATH_APP_NAME).extract()
        item['apk'] = response.xpath(XAPTH_APP_DOWNLOAD_URL).extract()

