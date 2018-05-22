# !/usr/bin/python
# coding: utf-8

from scrapy.exceptions import CloseSpider
from scrapy import Request, Spider
from ..items import BaiduItem

# Limit Number of app for each category
LIMIT_NUMBER_OF_APP = 100

# Category
CATEGORY = {
    '501': 0,
    '502': 0,
    '503': 0,
    '504': 0,
    '505': 0,
    '506': 0,
    '507': 0,
    '508': 0,
    '509': 0,
    '510': 0
}

# URL
DOMAIN = 'http://shouji.baidu.com'
CATEGORY_URL = 'http://shouji.baidu.com/software/'
SELECT_PAGE = '/list_%d.html'

# XPATH
XPATH_APP_URL = "//div[@class='app-bd']//li//a/@href"
XPATH_APP_CATEGORY = "//div[@class='nav']//span[5]"
XPATH_APP_NAME = "//div[@class='yui3-g']//h1[@class='app-name']/span"
XPATH_APK_URL = "//div[@class='yui3-g']//div[@class='area-download']/a/@href"
XPATH_APP_DETAIL = "//div[@class='yui3-g']//div[@class='detail']/span"


class AppSpider(Spider):
    name = 'baidu'

    def __init__(self, *args, **kwargs):
        super(AppSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [DOMAIN]

    # start with category urls
    def start_requests(self):
        for category_code in CATEGORY.keys():
            yield Request(
                url=CATEGORY_URL + category_code + SELECT_PAGE % 1,
                callback=self.parse,
                meta={
                    'pageNo': 1,
                    'cateNo': category_code
                }
            )

    # iterate all page numbers
    def parse(self, response):
        if response.status != 200:
            return
        # get all app urls on one page
        app_urls = response.xpath(XPATH_APP_URL)
        for app_url in app_urls:
            yield Request(
                url=CATEGORY_URL + app_url,
                callback=self.parse_app
            )
        # limit of number of apps
        cate_no = response.meta['cateNo']
        CATEGORY[cate_no] += len(app_urls)
        if CATEGORY[cate_no] > LIMIT_NUMBER_OF_APP:
            CloseSpider()
        # switch into the next page
        page_no = response.meta['pageNo'] + 1
        cate_no = response.meta['cateNo']
        yield Request(
            url=CATEGORY_URL + cate_no + SELECT_PAGE % page_no,
            callback=self.parse,
            meta={
                'pageNo': page_no,
                'cateNo': cate_no
            }
        )

    @staticmethod
    def parse_app(response):
        app_item = BaiduItem()
        app_item['name'] = response.xpath(XPATH_APP_NAME).extract()[0]
        app_item['category'] = response.xpath(XPATH_APP_CATEGORY).extract()[0]
        app_item['apk_url'] = response.xpath(XPATH_APK_URL).extract()[0]
        detail = response.xpath(XPATH_APP_DETAIL).extract()
        app_item['apk_size'] = detail[0]
        app_item['version'] = detail[1]
        app_item['download_count'] = detail[2]
