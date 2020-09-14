"""
@author: kid
@file: date.py
@time: 2020/1/6 17:21
"""
from datetime import datetime


def str2date(str):
    if str == '':
        return None
    return datetime.strptime(str, "%Y-%m-%d")


def date2str(date):
    if date is None:
        return ''
    return date.strftime("%Y-%m-%d")
