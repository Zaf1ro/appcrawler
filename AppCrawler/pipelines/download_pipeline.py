from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline


class FileDownloadItem(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item["file_urls"]:
            yield Request(file_url)

    def item_completed(self, results, item, info):
        file_paths = [x["path"] for ok, x in results if ok]
        print(file_paths)
        if not file_paths:
            raise DropItem("Item contains no file")
        return item

