# !/usr/bin/python
# coding: utf-8

from collections import OrderedDict
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
    def syntax(self):
        return ""

    def short_desc(self):
        return "check for the usage"

    def get_categories(self):
        categories = OrderedDict()
        for abbreviation, l in TYPE_ID.iteritems():
            categories[l[1]] = abbreviation
        return categories

    def run(self, args, opt):
        if len(args) != 0:
            raise UsageError("don't contains args")
        print("man & info - 360 App Store Spider")

        # 类别名称
        print("(1) Category Name:")
        for name, abbreviation in self.get_categories().iteritems():
            sys.stdout.write("  %-8s" % abbreviation)
            sys.stdout.flush()
            print(name)

        # 使用样例
        print("(2) Use Case:")
        print("scrapy crawl 360 -a cat=safe")   # unfinished
