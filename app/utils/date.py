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


def get_age_by_birth(birth_date):
    if birth_date is None:
        return None
    now_date = datetime.now().date()
    birth_date = str2date(birth_date).date()
    days = (now_date - birth_date).days
    return days//365


def get_birth_date_by_id_card(id_card):
    if id_card is None or len(id_card)!=18:
        return None
    year = id_card[6:10]
    month = id_card[10:12]
    day = id_card[12:14]
    if int(year)<1900 or int(month)>12 or int(day) > 31:
        return None
    birth_date =  year+'-'+month +'-'+day

    return birth_date