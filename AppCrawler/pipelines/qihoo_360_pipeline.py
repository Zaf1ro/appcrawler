# !/usr/bin/python
# coding: utf-8

from scrapy import Field, Item


class Qihoo360Item(Item):
    store = Field()
    name = Field()
    apk = Field()
    file_urls = Field()
    download_times = Field()
