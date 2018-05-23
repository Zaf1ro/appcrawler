# !/usr/bin/python
# coding: utf-8

import scrapy
import re
from scrapy import log
from scrapy.conf import settings
from collections import defaultdict
from ..items import GoogleItem

SEARCH_URL = 'https://play.google.com/store/search?q={keyword}&c=apps'
APP_URL_PREFIX = 'https://play.google.com'
APP_URL_XPATH = "//div[@class='details']/a[@class='card-click-target' and @tabindex='-1' and @aria-hidden='true']/@href"
LANG_OPTIONS = ['en', 'zh-cn', 'zh-tw', 'zh-hk']

# "//div[@class='info-container']/div[@class='document-title']/div/text()"
XPATH_APP_NAME = "//div[@class='info-box-top']/h1[@class='document-title']/div/text()"
XPATH_APP_CATEGORY = "//div/a[@class='document-subtitle category']/span/text()"
XPATH_APP_VERSION = "//div[@class='content' and @itemprop='softwareVersion']/text()"
XPATH_APP_DESCRIPTION = "//div[@class='show-more-content text-body' and @itemprop='description']//text()"
XPATH_APP_PUBLISH_DATE = "//div[@class='meta-info']/div[@itemprop='datePublished']/text()"
XPATH_APP_IMPROVEMENT = "//div[@class='details-section-contents show-more-container']/div[@class='recent-change']/text()"
XPATH_APP_SCORE_VALUE = "//div[@class='rating-box']/div[@class='score-container']/meta[@itemprop='ratingValue']/@content"
XPATH_APP_INSTALLS = "//div[@class='content' and @itemprop='numDownloads']/text()"


class PlayStoreSpider(scrapy.Spider):
    name = "googleplayspider"
    allowed_domains = ["play.google.com"]
    start_urls = []
    app_count = 0

    def __init__(self, keywords=None, lang='en', max_num=-1, account=None, password=None, outfile="item.csv", *args, **kwargs):
        super(PlayStoreSpider, self).__init__(*args, **kwargs)

        self.csvfile = open('test.csv', 'wb')
        self.workbook = UnicodeWriter(f=self.csvfile)
        fields = settings.get('APP_FIELDS', [])
        if fields:
            self.workbook.writerow(fields)

        # 语言设置
        if lang in self.LANG_OPTIONS:
            self.lang = lang
        else:
            self.man()
            raise Exception('"lang" -> "en","zh-cn"or"zh-tw"')

        # APP数量
        if isinstance(max_num, int):
            self.max_num = max_num
        else:
            raise Exception('max_apps -> int')
        self.outfile = outfile

        # 是否需要登录
        self.isLogin = False
        if account or password:
            if account and password:
                pattern = re.compile(r"^[a-z0-9]+([._\\-]*[a-z0-9])*@gmail.com", re.I)
                if pattern.match(account):
                    self.isLogin = True
                    self.account = account
                    self.password = password
                else:
                    raise GooglePlayException('account -> format error')
            else:
                raise GooglePlayException('miss account or password')

        # keyword
        self.isAll = False
        if keywords:
            if keywords == "all":
                self.start = 0
                self.count = 0

                self.isAll = True
                self.category_urls = defaultdict(list)
                self.categories = settings.get('APP_CATEGORIES', [])

                if self.categories:
                    for category in self.categories:
                        self.category_urls[category].append('https://play.google.com/store/apps/category/' + category + '/collection/topselling_paid')
                        self.category_urls[category].append('https://play.google.com/store/apps/category/' + category + '/collection/topselling_free')
                else:
                    raise GooglePlayException(u"读取category错误")
            else:
                keywords_array = keywords.split(',')
                for keyword in keywords_array:
                    self.start_urls.append(self.SEARCH_URL.format(keyword=keyword.strip()))
        else:
            self.man()
            raise GooglePlayException('"keywords are required"')

    def start_requests(self):
        # if self.isLogin:
        #     self.redirect_to_login_page()

        if self.isAll:
            for category in self.categories:
                for url in self.category_urls[category]:
                    yield scrapy.Request(url, callback=self.parse_category_page)
        else:
            for url in self.start_urls:
                yield scrapy.FormRequest(
                    url,
                    formdata={
                        'ipf': '1',
                        'xhr': '1',
                    },
                    callback=self.parse_search_page)

    @staticmethod
    def man():
        print("\n")
        print(">>> man : scrapy googleplay -a keyword=<keywords_separated_by_commas> [options]")
        print(">>> Options : ")
        print(">>> -a download_delay=<seconds>      unit: second")
        print(">>> -a language=<lang>               only support:en,zh-cn,zh-tw, default:en")
        print(">>> -a max_apps=<max_num>            max number of app")

    def parse(self, response):
        pass

    def parse_category_page(self, response):
        app_urls = response.xpath(APP_URL_XPATH).extract()
        self.count += len(app_urls)

        for url in app_urls:
            yield scrapy.Request(APP_URL_PREFIX + url + "&hl={lang}".format(lang=self.lang),
                                 callback=self.parse_app_url)

        if len(app_urls) == 60:
            self.start += 60
            yield scrapy.FormRequest(
                url=response.url,
                callback=self.parse_category_page,
                formdata={
                    'start': '%s' % self.start,
                    'num': '60',
                    'ipf': '1',
                    'xhr': '1',
                }
            )
        else:
            print(response.url, self.count)
            self.start = 0
            self.count = 0

    def redirect_to_login_page(self):
        return [scrapy.Request(
            'https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/%3Fgws_rd%3Dssl',
            callback=self.login)]

    def login(self, response):
        match = re.search(r'<input\s+name="GALX"[\s\S]+?value="(.+?)">', response.body, flags=re.M)

        galx = ''
        if match:
            galx = match.group(1)
        return [
            scrapy.FormRequest(
                "https://accounts.google.com/ServiceLoginAuth",
                formdata={
                    'Email': self.account,
                    'Passwd': self.password,
                    'PersistentCookie': 'yes',
                    'GALX': galx,
                    'hl': 'en',
                    'continue': 'http://www.google.com/?gws_rd=ssl',
                },
                callback=self.after_login()
            )
        ]

    def parse_search_page(self, response):
        app_urls = response.xpath(APP_URL_XPATH).extract()

        for url in app_urls:
            yield scrapy.Request(APP_URL_PREFIX + url + "&hl={lang}".format(lang=self.lang),
                                 callback=self.parse_app_url)

        match = re.search(r"'\[.*\\42((?:.(?!\\42))*:S:.*?)\\42.*\]\\n'", response.body)
        if match:
            page_token = match.group(1).replace('\\\\', '\\').decode('unicode-escape')
        else:
            page_token = None
        if page_token is not None:
            yield scrapy.FormRequest(
                response.url,
                formdata={
                    'ipf': '1',
                    'xhr': '1',
                    'pagTok': page_token,
                },
                callback=self.parse_search_page)

    def parse_app_url(self, response):
        if self.max_num > 0 and (self.app_count >= self.max_num):
            log.msg("Max Item reached", level=log.DEBUG)
            self.crawler.engine.close_spider(self, response=response)

        app_item = GoogleItem()
        app_item['name'] = response.xpath(XPATH_APP_NAME).extract()[0]
        app_item['app_id'] = (response.url.split("id=")[1]).split("&")[0]
        app_item['category'] = response.xpath(XPATH_APP_CATEGORY).extract()[0]
        app_item['version'] = response.xpath(XPATH_APP_VERSION).extract()[0].strip()
        app_item['description'] = response.xpath(XPATH_APP_DESCRIPTION).extract()[1]
        app_item['app_url'] = response.url
        app_item['update_date'] = response.xpath(XPATH_APP_PUBLISH_DATE).extract()[0]

        improvement = ""
        improvements = response.xpath(XPATH_APP_IMPROVEMENT).extract()
        for data in improvements:
            improvement += data + u'\n'

        app_item['score'] = response.xpath(XPATH_APP_SCORE_VALUE).extract()[0]
        app_item['download_count'] = response.xpath(XPATH_APP_INSTALLS).extract()[0].strip()

        # self.workbook.writerow(["GooglePlay", app_item["name"], app_item["app_id"], app_item["category"],
        #                         app_item["version"], app_item["description"], app_item["improvement"],
        #                         app_item["url"], app_item["update_date"], app_item["score"], app_item["download_count"]])

        self.app_count += 1
