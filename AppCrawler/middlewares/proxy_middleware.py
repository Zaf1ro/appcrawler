# !/usr/bin/python
# coding: utf-8

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64


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