# !/usr/bin/python
# coding: utf-8

from scrapy.exporters import CsvItemExporter, JsonItemExporter
from scrapy.conf import settings


# Save item into json file
class JsonExportPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        return pipeline

    def open_spider(self, spider):
        file = open('/tmp/%s.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# Save the item into csv file
class CsvExporter(CsvItemExporter):
    # def __init__(self, file, **kwargs):
    #     super(CsvExporter, self).__init__(
    #         file,
    #         include_headers_line=True,
    #         delimiter=',',
    #         **kwargs
    #     )
    def __init__(self, *args, **kwargs):
        super(CsvExporter, self).__init__(*args, **kwargs)

    # def __init__(self, switcher):
    #     self.switcher = switcher
    #     self.csv_files = None
    #     self.csv_exporter = None
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         switcher=crawler.settings.get('STORE_FIELDS')
    #     )
    #
    # def open_spider(self, spider):
    #     csv = open('/tmp/%s_items.csv' % spider.name, 'w+b')
    #     self.csv_files[spider] = csv
    #     export_fields = self.switcher[spider.name]
    #     self.csv_exporter = CsvItemExporter(csv, export_fields=export_fields)
    #     self.csv_exporter.start_exporting()
    #
    # def close_spider(self, spider):
    #     self.csv_exporter.finish_exporting()
    #     csv = self.csv_files.pop(spider)
    #     csv.close()
    #
    # def process_item(self, item, spider):
    #     self.csv_exporter.export_item(item)
    #     return item