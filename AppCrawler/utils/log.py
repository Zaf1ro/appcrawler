#!/usr/bin
# -*- coding: utf-8 -*-

import logging
import os
import time
"""
NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
"""


LEVEL = {
    'c': logging.CRITICAL,
    'e': logging.ERROR,
    'w': logging.WARNING,
    'i': logging.INFO,
    'd': logging.DEBUG,
    'n': logging.NOTSET,
}

LOG_PREFIX = time.strftime("\\%Y-%m-%d_", time.localtime())


def get_log_path(mark):
    logdir = os.path.join(os.getcwd(), 'tmp')
    if os.path.exists(logdir):
        return logdir + LOG_PREFIX + str(mark) + '.log'
    else:
        os.mkdir('tmp')


def get_level(level):
    if not level:
        level = logging.ERROR
    elif level[0].lower() in LEVEL.keys():
        level = LEVEL[level[0].lower()]
    else:
        level = logging.DEBUG
    return level


def get_log(name, min_level, mark='default'):
    logger = logging.getLogger(name)
    logger.setLevel(get_level(min_level))
    print(logger.level)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

    fh = logging.FileHandler(get_log_path(mark))
    ch = logging.StreamHandler()

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
