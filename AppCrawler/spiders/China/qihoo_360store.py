# !/usr/bin/python
# coding: utf-8

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from AppCrawler.pipelines.qihoo_360_pipeline import Qihoo360Item
from AppCrawler.spiders import *
from download import *

# Category
DOMAIN = "http://zhushou.360.cn"
CATEGORY_URL = "http://zhushou.360.cn/list/index/cid/"
ORDER_BY_DOWNLOAD_URL = "/order/download/?page="
APP_URL = "http://zhushou.360.cn/detail/index/soft_id/"

# XPATH
APP_URL_XPATH = "//*[@id='iconList']/li/h3/a/@href"  # OK
DOWNLOAD_URL_XPATH = "//*[@id='app-info-panel']/div/dl/dd/a/@href"  # OK
DOWNLOAD_TIMES_XPATH = "//*[@id='app-info-panel']/div/dl/dd/div/span[3]/text()"  # OK
APP_NAME_XPATH = "//*[@id='app-name']/span/@title"  # OK


class MainSpider(scrapy.Spider):
    name = "360crawler"

    def __init__(self, cat=None, save=None, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["360.cn"]
        self.cat = cat
        self.cats, self.reverse_id = self.handle_cat(cat)
        print(self.cats)
        print(self.reverse_id)
        # self.save - 保存方式 - unfinished

        self.start_urls = [
            DOMAIN,
        ]

        self.fail_log = open("log.txt", "w+")

    @staticmethod
    def handle_cat(cat):
        cats = []
        reverse_id = {}
        for l in TYPE_ID.itervalues():
            reverse_id[l[0]] = l[1]
        if not cat:
            for l in TYPE_ID.itervalues():
                cats.append(l[0])
        else:
            # 多个cat问题 - unfinished
            if cat in TYPE_ID.iterkeys():
                cats.append(TYPE_ID[cat][0])
            else:
                raise CloseSpider(u"未找到合适的类别, 请使用\"scrapy help\"来查看使用说明!")
        return cats, reverse_id

    def parse(self, response):

        # 网络情况
        if response.status != 200:
            CloseSpider(u"网络状况有问题.")

        # 类型
        while True:
            cat = self.cats.pop()
            t1, printable_time = get_current_time()
            print(printable_time + " : Start to crawl " + self.reverse_id[cat])

            for i in range(20, 30):     # 页数
                yield Request(url=CATEGORY_URL + str(cat) + ORDER_BY_DOWNLOAD_URL + str(i), callback=self.parse_page,
                              meta={'dirname': self.reverse_id[cat], 'numofpage': i})

            t2, printable_time = get_current_time()
            print(printable_time + " : End to crawl " + self.reverse_id[cat] + " taking %d s" % (
                    get_interval_time(t1, t2))
                  )

            if not self.cats:
                break

        # self.fail_log.close()

    def parse_page(self, response):  # 处理某个类别的单个页面
        dirname = response.meta['dirname'] + str(response.meta['numofpage'])
        path = os.path.join(os.path.abspath(os.getcwd()), 'apk')
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(path, dirname)
        if not os.path.exists(path):
            os.mkdir(path)

        print(path)

        app_urls = response.xpath(APP_URL_XPATH).extract()
        for url in app_urls:
            yield Request(url=DOMAIN + url, callback=self.parse_app, meta={"store": "360", "path": path})

    def parse_app(self, response):  # 处理单个应用
        item = Qihoo360Item(store=response.meta["store"])
        item['name'] = response.xpath(APP_NAME_XPATH).extract()[0]
        original_apk_url = (response.xpath(DOWNLOAD_URL_XPATH).extract()[0]).split("/")
        item['file_urls'] = "http://shouji.360tpcdn.com/" + \
                            original_apk_url[8] + '/' + \
                            original_apk_url[9] + '/' + \
                            original_apk_url[10]
        yield item

