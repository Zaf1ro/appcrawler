#!/usr/bin
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
from thread import ThreadPool
from threading import Thread

"""
start_download - download_single_apk - download_url_urllib
"""

THREAD_POOL_SIZE = 3

total = 0   # total number of jobs
done = 0    # the number of finished jobs
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


def download_url_urllib(url, filepath, proxy=None):
    if (not filepath) or (not url):
        print 'Url or filepath is not valid, resouce cannot be downloaded.'
        return

    fname = os.path.basename(filepath)

    try:
        # 设置代理
        proxy_handler = urllib2.ProxyHandler(proxy) if proxy else None
        opener = None
        if proxy_handler:
            opener = urllib2.build_opener(proxy_handler)

        urllib2.install_opener(opener)
        r = urllib2.urlopen(url, timeout=30)

        if r.getcode() == 200:
            total_length = int(r.info().getheader('Content-Length').strip())

            done_length = 0
            chunk_size = 1024
            with open(filepath, 'wb') as f:
                while True:
                    chunk = r.read(chunk_size)
                    done_length += len(chunk)
                    if not chunk:
                        print '\nfinished: %s' % fname
                        return 1
                    f.write(chunk)
                    sys.stdout.write('\r%.2f%%' % (done_length * 1.0 / total_length))
                    # if show_progress:
                    #     fill_download_progress(fname, total_length, done_length)
        else:
            print "HTTP Status %d . APK: %s " % (r.status_code, fname)
            return 0

    except Exception, err:
        print "Downloading Apk %s timeout!" % fname
        return 1


# --- download single apk ---

def download_single_apk(apk):
    global done, progress

    if (not apk.filename) or (not apk.dl_link):
        print 'Apk [id:%s] cannot be downloaded' % apk.fname
        return
    mp3_file = apk.abs_path

    retry = 5
    dl_result = 0  # download return code
    print "Downloading: %s" % apk.dl_link
    while retry > 0:
        retry -= 1
        print "Start downloading: %s retry: %d" % (mp3_file, 5 - retry)

        # do the actual downloading
        dl_result = download_url_urllib(apk.dl_link, mp3_file, proxy=get_proxy(apk))

        if dl_result:  # success
            apk.success = True
            fill_done2show(apk)     # 信息提取 - unfinished
            # remove from progress
            del progress[apk.filename]
            print "Finished: %s" % mp3_file
            break
        else:  # not success
            # remove from progress
            del progress[apk.filename]
            if os.path.exists(apk.abs_path):
                # remove file if already exists
                print '[DL_apk] remove incompleted file : ' + apk.abs_path
                os.remove(apk.abs_path)
                # retry

    done += 1  # no matter success of fail, the task was done
    if not dl_result:
        # if it comes here, 5 retries run out
        fill_failed_list(apk)       # unfinished


class Downloader(Thread):
    def __init__(self, apks, pool):
        Thread.__init__(self)
        self.apks = apks
        self.pool = pool

    def run(self):
        global progress
        for apk in self.apks:
            self.pool.add_task(download_single_apk, apk)
        self.pool.wait_completion()


# --- main ---

def start_download(apks, filter):
    global total
    total = len(apks)
    print 'init thread pool (%d) for downloading' % THREAD_POOL_SIZE
    pool = ThreadPool(THREAD_POOL_SIZE)
    downloader = Downloader(apks, pool)
    downloader.start()

    # while done < total:
    #     time.sleep(1)
    #     print_progress()
