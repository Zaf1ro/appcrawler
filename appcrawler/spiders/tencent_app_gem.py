# !/usr/bin/python
# coding: utf-8

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from ..items import TencentAppGemItem


# Category
CATEGORY_tencent = [
    [103, u"视频"],
    [101, u"音乐"],
    [122, u"购物"],
    [102, u"阅读"],
    [112, u"导航"],
    [106, u"社交"],
    [104, u"摄影"],
    [110, u"新闻"],
    [115, u"工具"],
    [119, u"美化"],
    [111, u"教育"],
    [107, u"生活"],
    [118, u"安全"],
    [108, u"旅游"],
    [100, u"儿童"],
    [114, u"理财"],
    [117, u"系统"],
    [109, u"健康"],
    [109, u"娱乐"],
    [109, u"办公"],
    [109, u"通讯"],
]
Domain = "http://android.app.qq.com"
CATEGORY_URL = "http://android.app.qq.com/myapp/category.htm?orgame=1&categoryId="

XPATH_CATEGORY = "/html/body/div[3]/div[2]/ul/li[1]/div/a"
XPATH_APP_DOWNLOAD_URL = '//*[@id="J_DetDataContainer"]/div/div[1]/div[3]/a[2]/@data-apkurl'
XPATH_APP_NAME = '//*[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[1]/div[1]'


class MAINSpider(Spider):
    name = "tencent"

    def __init__(self, cat=None, save=None, *args, **kwargs):
        super(MAINSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["qq.com"]
        self.categories = handle_category(cat, 'tencent')
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
                yield Request(url=CATEGORY_URL + str(pair[0]), callback=self.parse_page)

            t2, printable_time = get_current_time()
            print(printable_time + " : End to crawl " + pair[1] + " taking %d s" % (get_interval_time(t1, t2)))

    def parse_single_category(self, response):
        app_urls = response.xpath(XPATH_APP_URL).extract()
        for url in app_urls:
            yield Request(url=Domain + url, callback=self.parse_app, meta={"store": "360"})

    @staticmethod
    def parse_single_app(response):
        item = Item_tencent()
        item['name'] = response.xpath(XPATH_APP_NAME).extract()
        item['apk'] = response.xpath(XAPTH_APP_DOWNLOAD_URL).extract()
