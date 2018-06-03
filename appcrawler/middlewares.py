# !/usr/bin/python
# coding: utf-8

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


# Start your middleware class
class ProxyMiddleware(object):
    PROXIES = [{'ip_port': '168.63.249.35:80', 'user_pass': ''},
               {'ip_port': '162.17.98.242:8888', 'user_pass': ''},
               {'ip_port': '70.168.108.216:80', 'user_pass': ''},
               {'ip_port': '45.64.136.154:8080', 'user_pass': ''},
               {'ip_port': '149.5.36.153:8080', 'user_pass': ''},
               {'ip_port': '185.12.7.74:8080', 'user_pass': ''},
               {'ip_port': '150.129.130.180:8080', 'user_pass': ''},
               {'ip_port': '185.22.9.145:8080', 'user_pass': ''},
               {'ip_port': '200.20.168.135:80', 'user_pass': ''},
               {'ip_port': '177.55.64.38:8080', 'user_pass': ''}, ]

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"

        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass


class SwitchUserAgentMiddleware(UserAgentMiddleware):
    user_agent_list = [
        # MAC
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',

        # IE
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',

        # Firefox
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',

        # Opera
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',

        # Other
        'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
    ]

    def __init__(self, user_agent=''):
        super(SwitchUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent

    def get_user_agent(self, spider):
        if hasattr(spider, 'user_agent'):
            return spider.user_agent
        elif self.user_agent:
            return self.user_agent

        return random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        ua = self.get_user_agent(spider)
        if ua:
            request.headers.setdefault('User-Agent', ua)

