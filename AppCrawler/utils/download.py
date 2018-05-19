# !/usr/bin/python
# coding: utf-8

import os
import sys
from urllib.request import urlopen, urlretrieve

"""
start_download - download_single_apk - download_url_urllib
"""

THREAD_POOL_SIZE = 3

total = 0  # total number of jobs
done = 0  # the number of finished jobs
unsucess_list = []
success_list = []


# --- download_url_urllib ---
def Schedule(downloaded_block, block_size, total_size):
    """
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   """
    per = 100.0 * downloaded_block * block_size / total_size
    if per > 100:
        per = 100
    sys.stdout.write('\r%.2f%%' % per)


def download_single_apk(url, name):
    cur_path = os.path.abspath(os.getcwd())
    apk_path = os.path.join(cur_path, 'AppCrawler')
    urlretrieve(url, apk_path + '\\apk\\' + name + '.apk', Schedule)


def download_urllib2(url, path, fname):
    fname += '.apk'
    filepath = os.path.join(path, fname)
    if os.path.exists(filepath):
        print("%s already existed" % fname)
        return 1

    i = 1
    while i < 3:
        try:
            # 设置代理
            # proxy_handler = urllib2.ProxyHandler(proxy) if proxy else None
            # opener = None
            # if proxy_handler:
            #     opener = urllib2.build_opener(proxy_handler)
            # urllib2.install_opener(opener)

            r = urlopen(url, timeout=30)

            if r.getcode() == 200:
                total_length = int(r.info().getheader('Content-Length').strip())

                done_length = 0
                chunk_size = 1024
                with open(filepath, 'wb') as f:
                    while True:
                        chunk = r.read(chunk_size)
                        done_length += len(chunk)
                        if not chunk:
                            print('\nfinished: %s' % fname)
                            return 1
                        f.write(chunk)
                        sys.stdout.write('\r%2f%%' % (done_length * 1.0 / total_length))
            else:
                if os.path.exists(filepath):
                    os.remove(filepath)
                print("Failed to connect. APK: %s" % fname)
                i += 1
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            print("Downloading Apk %s timeout!" % fname)
            i += 1

        return 0


# if __name__ == "__main__":
