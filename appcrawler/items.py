# !/usr/bin/python
# coding: utf-8

from scrapy import Field, Item


class QihooItem(Item):
    category = Field()
    name = Field()
    rating = Field()
    apk_url = Field()
    download_count = Field()
    apk_size = Field()


class TencentItem(Item):
    name = Field()
    apk_size = Field()
    apk_url = Field()
    download_count = Field()
    seller = Field()
    rating = Field()
    category = Field()


class BaiduItem(Item):
    name = Field()
    category = Field()
    apk_url = Field()
    apk_size = Field()
    version = Field()
    download_count = Field()


class GoogleItem(Item):
    name = Field()
    app_id = Field()
    category = Field()
    version = Field()
    description = Field()
    improvement = Field()
    app_url = Field()
    update_date = Field()
    score = Field()
    download_count = Field()


class AppleItem(Item):
    name = Field()          # name of app
    seller = Field()        # name of seller
    size = Field()          # size of apk
    category = Field()      # category of app
    is_iphone = Field()     # available on iPhone
    is_ipad = Field()       # available on iPad
    is_ipod = Field()       # available on iPod
    languages = Field()     # supported language
    rating = Field()        # rating of app
    price = Field()         # price of app
