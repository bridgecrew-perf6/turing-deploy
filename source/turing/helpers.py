# coding: utf-8

import os
import errno
import re
import time
import random


def get_day(timestamp):
    FORY = '%d'
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def format_date(timestamp):
    FORY = '%Y-%m-%d @ %H:%M'
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str

def get_year():
    timestamp = int(time.time())
    FORY = '%Y'
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str


def get_month():
    timestamp = int(time.time())
    FORY = '%m'
    time.tzset()
    format_str = time.strftime(FORY, time.localtime(timestamp))
    return format_str



def regex(pattern, data, flags=0):
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def url(data):
    pattern = (
        r'(?i)^((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$')
    return regex(pattern, data, re.IGNORECASE)


def username(data):
    pattern = r'^[a-zA-Z0-9]+$'
    return regex(pattern, data)


def force_int(value, default=1):
    try:
        return int(value)
    except TypeError:
        return default


def gen_random_str(n=6):
    return ''.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba', n))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def remove_file(file_path):
    if not os.path.isfile(file_path):
        return
    os.remove(file_path)

