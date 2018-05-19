# !/usr/bin/python
# coding: utf-8

from scrapy import Field, Item


class Qihoo360StoreItem(Item):
    store = Field()
    name = Field()
    apk = Field()
    file_urls = Field()
    download_times = Field()


class TencentAppGemItem(Item):
    store = Field()
    name = Field()
    apk = Field()
    file_urls = Field()
    download_times = Field()


class BaiduMobileAssistantItem(Item):
    store = Field()
    name = Field()
    apk = Field()
    file_urls = Field()
    download_times = Field()


class GooglePlayStoreItem(Item):
    market = Field()
    name = Field()
    app_id = Field()
    category = Field()
    version = Field()
    description = Field()
    improvement = Field()
    url = Field()
    update_date = Field()
    score = Field()
    download_count = Field()


class AppleAppStoreItem(Item):
    name = Field()          # name of app
    is_iphone = Field()     #
    is_ipad = Field()
    is_ipod = Field()
    description = Field()
    artwork = Field()
    subcategory = Field()
    price = Field()
    release_date = Field()
    version = Field()
    size = Field()
    languages = Field()
    seller = Field()
    seller_link = Field()
    copyright = Field()
    rating = Field()
    requirements = Field()
    reviews = Field()
    screenshots = Field()
