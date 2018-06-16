# coding=utf-8

from os.path import abspath, dirname


def get_data_files():
    path = abspath(dirname(__file__))
    return path


DATA_FILES_PATH = get_data_files()
