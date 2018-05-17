# !/usr/bin/python
# coding: utf-8

from scrapy.spider import BaseSpider
from AppCrawler.pipelines.qihoo_360_pipeline import Qihoo360Item
# from ..pipelines.file_download_item import FileDownloadItem


class TestSpider(BaseSpider):
    name = "ietf"
    allowed_domains = ["ietf.org"]
    start_urls = (
        'http://www.ietf.org/',
    )

    def parse(self, response):
        pass


