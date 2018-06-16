# coding=utf-8

import uuid
import os
import shutil
import stat
from datetime import datetime


def force_int(value, default=1):
    try:
        return int(value)
    except TypeError:
        return default

def replace_dir(dir_path):
    isExists = os.path.exists(dir_path)
    if isExists:
        shutil.rmtree(dir_path)
    try:
        os.makedirs(dir_path)
        # mode:777
        os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except Exception as e:
        print(e)
        return False
    return True

def create_dir(dir_path):
    isExists = os.path.exists(dir_path)
    if not isExists:
        try:
            os.makedirs(dir_path)
            # mode:777
            os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except Exception as e:
            print(e)
            return False
    return True


# Token utilities

def new_token():
    """generator for new random tokens

    For now, just UUIDs.
    """
    return uuid.uuid4().hex


def url_path_join(*pieces):
    """Join components of url into a relative url

    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place

    Copied from notebook.utils.url_path_join
    """
    initial = pieces[0].startswith('/')
    final = pieces[-1].endswith('/')
    stripped = [s.strip('/') for s in pieces]
    result = '/'.join(s for s in stripped if s)

    if initial:
        result = '/' + result
    if final:
        result += '/'
    if result == '//':
        result = '/'

    return result


def convert_str2list(query_string):
    query_list = query_string.strip().split(" ")
    res = []
    for q in query_list:
        if not q == "":
            res.append(q)
    return res


def get_local_time():
    return datetime.now()


def generate_uuid_name():
    return str(uuid.uuid1()).replace('-', '')

def timestamp2localtime(timestamp):
    dateArray = datetime.utcfromtimestamp(int(timestamp))
    return dateArray.strftime("%Y-%m-%d %H:%M:%S")
