# !/usr/bin/python
# coding: utf-8


# Google XPATH
XPATH_google = {
    'name': "//div[@class='info-box-top']/h1[@class='document-title']/div/text()",
    'category': "//div/a[@class='document-subtitle category']/span/text()",
    'version': "//div[@class='content' and @itemprop='softwareVersion']/text()",
    'description': "//div[@class='show-more-content text-body' and @itemprop='description']//text()",
    'update_date': "//div[@class='meta-info']/div[@itemprop='datePublished']/text()",
    'score': "//div[@class='rating-box']/div[@class='score-container']/meta[@itemprop='ratingValue']/@content",
    'improvement': "//div[@class='details-section-contents show-more-container']/div[@class='recent-change']/text()",
    'downloads': "//div[@class='content' and @itemprop='numDownloads']/text()"
}

# 360 XPATH
XPATH_360 = {
    'app_url': "//*[@id='iconList']/li/h3/a/@href",    # OK
    'downloads': "//*[@id='app-info-panel']/div/dl/dd/div/span[3]/text()",   # OK
    'download_url': "//*[@id='app-info-panel']/div/dl/dd/a/@href",  # OK
    'name': "//*[@id='app-name']/span/@title"   # OK
}


XPATH_ = {
    'name' =
}