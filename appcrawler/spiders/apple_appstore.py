# !/usr/bin/python
# coding: utf-8

import scrapy
from ..items import AppleAppStoreItem
import datetime


# TODO: limit of pages of each category
CATEGORY = {
    'book': 'http://itunes.apple.com/us/genre/ios-books/id6018?mt=8',
    'business': 'https://itunes.apple.com/us/genre/ios-business/id6000?mt=8',
    'education': 'https://itunes.apple.com/us/genre/ios-education/id6017?mt=8',
    'entertainment': 'https://itunes.apple.com/us/genre/ios-entertainment/id6016?mt=8',
    'finance': 'https://itunes.apple.com/us/genre/ios-finance/id6015?mt=8',
    'eat': 'https://itunes.apple.com/us/genre/ios-food-drink/id6023?mt=8',
    'game': 'https://itunes.apple.com/us/genre/ios-games/id6014?mt=8',
    'health': 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8',
    'lifestyle': 'https://itunes.apple.com/us/genre/ios-lifestyle/id6012?mt=8',
    'magazine': 'https://itunes.apple.com/us/genre/ios-magazines-newspapers/id6021?mt=8',
    'medical': 'https://itunes.apple.com/us/genre/ios-medical/id6020?mt=8',
    'music': 'http://itunes.apple.com/us/genre/ios-music/id6011?mt=8',
    'navigation': 'http://itunes.apple.com/us/genre/ios-navigation/id6010?mt=8',
    'news': 'http://itunes.apple.com/us/genre/ios-news/id6009?mt=8',
    'newsstand': 'http://itunes.apple.com/us/genre/ios-newsstand/id6021?mt=8',
    'photo': 'http://itunes.apple.com/us/genre/ios-photo-video/id6008?mt=8',
    'productivity': 'http://itunes.apple.com/us/genre/ios-productivity/id6007?mt=8',
    'reference': 'http://itunes.apple.com/us/genre/ios-reference/id6006?mt=8',
    'social': 'http://itunes.apple.com/us/genre/ios-social-networking/id6005?mt=8',
    'sports': 'http://itunes.apple.com/us/genre/ios-sports/id6004?mt=8',
    'travel': 'http://itunes.apple.com/us/genre/ios-travel/id6003?mt=8',
    'utilities': 'http://itunes.apple.com/us/genre/ios-utilities/id6002?mt=8',
    'weather': 'http://itunes.apple.com/us/genre/ios-weather/id6001?mt=8',
}

# XPATH in app category page
XPATH_INITIAL_LETTER = "//*[@id='selectedgenre']/ul[1]//a"
XPATH_PAGE = "//*[@id='selectedgenre']/ul[2]//a"

# XPATH in app page
XPATH_APP_NAME = "//header/h1/text()"   # 6 results
XPATH_APP_INFO = "//dl[@class='information-list information-list--app medium-columns']//dd"  # 1 results
XPATH_APP_VERSION = "//p[@class='l-column small-6 medium-12 whats-new__latest__version']"
XPATH_APP_RATING = "//div/div[1]/h3/span"


class AppStoreSpider(scrapy.Spider):
    name = 'appstore'
    allowed_domains = ['itunes.apple.com']
    start_urls = CATEGORY.values()

    def __init__(self, keywords=None, *args, **kwargs):
        super(AppStoreSpider, self).__init__(*args, **kwargs)

    # start to parse requests
    def start_requests(self):
        for category_url in CATEGORY.values():
            yield scrapy.Request(category_url, callback=self.parse)

    # iterate apps by category
    def parse(self, response):

        category = response.select('//title/text()').extract()[0].split('-')[0].strip()
        idx = 0
        for url, name in zip(hxs.select('//div[contains(@class,"column")]/ul/li/a/@href').extract(), hxs.select('//div[contains(@class,"column")]/ul/li/a/text()').extract()):
            if not '/app/' in url:
                continue
            i = AppItem()
            i['name'] = name
            i['url'] = url
            i['id'] = url.split('/')[-1].split('?')[0]
            i['category'] = category
            i['last_update'] = datetime.date.today().isoformat()
            i['store'] = 'appstore'
            idx += 1
            yield i

    # iterate apps by initial letter
    def iterate_by_initial_letter(self):
        pass

    # iterate apps by num of page
    def iterate_by_page(self):
        pass

    @staticmethod
    def parse_app(response):  # parse_app
        app_item = AppleAppStoreItem()
        app_item['name'] = response.xpath(XPATH_APP_NAME).extract()[3]
        app_info = response.xpath(XPATH_APP_INFO).extract()
        app_item['seller'] = app_info[0]
        app_item['size'] = app_info[1]      # erase 'MB'
        app_item['category'] = app_info[2]

        # Check for compatibility
        compatibility = app_info[3]
        app_item['is_iphone'] = 'iPhone' in compatibility
        app_item['is_ipad'] = 'iPad' in compatibility
        app_item['is_ipod'] = 'iPod' in compatibility

        app_item['languages'] = app_info[4]     # English, Dutch, French, German, Italian
        app_item['age_rating'] = app_info[5]    # 4+
        app_item['price'] = app_info[7]         # Free

        yield app_item

