"""
@author: yours
@file: past_history.py
@time: 2020-09-04 21:03
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db
from app.models.base_line import  PastHis

api = Redprint('past_history')

@api.route('/<int:pid>',methods = ['GET'])
def get_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first()
    return Success(data=past_history if past_history else {})


@api.route('',methods = ['POST'])
def add_past_history():
    data = request.get_json()
    if 'id' in data:
        pastHis = PastHis.query.get_or_404(data['id'])
        data['pid'] = pastHis.pid
    json2db(data, PastHis)
    return Success()