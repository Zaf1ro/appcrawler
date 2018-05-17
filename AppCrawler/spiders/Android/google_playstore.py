# !/usr/bin/python
# coding: utf-8


import scrapy
import re
from items import AppItem
from scrapy import log
import csv, codecs, cStringIO
from scrapy.conf import settings
from collections import defaultdict


class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



class GooglePlayException(Exception):

    def __init__(self, error_statement):
        self.__error = error_statement

    def __str__(self):
        return repr(self.__error)


class PlayStoreSpider(scrapy.Spider):
    name = "googleplayspider"
    allowed_domains = ["play.google.com"]
    start_urls = []

    SEARCH_URL = 'https://play.google.com/store/search?q={keyword}&c=apps'
    APP_URL_PREFIX = 'https://play.google.com'
    APP_URL_XPATH = "//div[@class='details']/a[@class='card-click-target' and @tabindex='-1' and @aria-hidden='true']/@href"
    LANG_OPTIONS = ['en', 'zh-cn', 'zh-tw', 'zh-hk']

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
            raise GooglePlayException('"lang" -> "en","zh-cn"or"zh-tw"')

        # APP数量
        if isinstance(max_num, int):
            self.max_num = max_num
        else:
            raise GooglePlayException('max_apps -> int')
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

    # 开始全局搜索
    # def redirect_to_category_page(self):
    #
    #     print 2

    def parse_category_page(self, response):

        app_urls = response.xpath(self.APP_URL_XPATH).extract()
        self.count += len(app_urls)

        for url in app_urls:
            yield scrapy.Request(self.APP_URL_PREFIX + url + "&hl={lang}".format(lang=self.lang),
                                 callback=self.parse_app_url)

        if len(app_urls) == 60:
            self.start += 60
            yield scrapy.FormRequest(
                response.url,
                formdata={
                    'start': '%s' % self.start,
                    'num': '60',
                    'ipf': '1',
                    'xhr': '1',
                },
                callback=self.parse_category_page
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

    def parse_search_page(self, response):
        app_urls = response.xpath(self.APP_URL_XPATH).extract()

        for url in app_urls:
            yield scrapy.Request(self.APP_URL_PREFIX + url + "&hl={lang}".format(lang=self.lang),
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

        appitem = AppItem()
        appitem['market'] = "GooglePlay"
        appitem['name'] = response.xpath(AppItem.APP_NAME).extract()[0]
        appitem['app_id'] = (response.url.split("id=")[1]).split("&")[0]
        appitem['category'] = response.xpath(AppItem.APP_CATEGORY).extract()[0]
        appitem['version'] = response.xpath(AppItem.APP_VERSION).extract()[0].strip()
        appitem['description'] = response.xpath(AppItem.APP_DESCRIPTION).extract()[1]
        appitem['url'] = response.url
        appitem['update_date'] = response.xpath(AppItem.APP_PUBLISH_DATE).extract()[0]

        improvement = ""
        improvements = response.xpath(AppItem.APP_IMPROVEMENT).extract()
        for data in improvements:
            improvement += data + u'\n'
        appitem['improvement'] = improvement

        appitem['score'] = response.xpath(AppItem.APP_SCORE_VALUE).extract()[0]
        appitem['download_count'] = response.xpath(AppItem.APP_INSTALLS).extract()[0].strip()

        self.workbook.writerow(["GooglePlay", appitem["name"], appitem["app_id"], appitem["category"],
                                appitem["version"], appitem["description"], appitem["improvement"],
                                appitem["url"], appitem["update_date"], appitem["score"], appitem["download_count"]])

        self.app_count += 1
