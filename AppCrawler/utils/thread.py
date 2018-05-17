#!/usr/bin
# -*- coding: utf-8 -*-


from threading import Thread
from Queue import Queue


class ThreadPool(object):
    def __init__(self, size):
        self.tasks = Queue(size)
        for i in range(size):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


class Worker(Thread):
    def __init__(self, taskQueue):
        Thread.__init__(self)
        self.tasks = taskQueue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception, e:
                print str(e)
            finally:
                self.tasks.task_done()


class Apk(object):

    def __init__(self, fname=None, dl_link=None, abs_path=None):
        self.fname = fname
        self.dl_link = dl_link
        self.abs_path = abs_path
        self.success = False
        self.store = ''
