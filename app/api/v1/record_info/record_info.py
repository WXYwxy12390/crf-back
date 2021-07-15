"""
@author: yours
@file: record_info.py
@time: 2020-09-16 20:44
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success, APIException
from app.libs.error_code import ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, json2db_add
from app.models.therapy_record import TreRec

api = Redprint('record_info')


@api.route('/nav/<int:pid>', methods=['GET'])
def get_record_info_nav(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    return Success(data=len(tre_recs))


@api.route('/<int:pid>/<int:treIndex>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_record_info(pid, treIndex):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    if treIndex > len(tre_recs) + 1 or treIndex < 1:
        return ParameterException(msg='treIndex wrong')
    for tre_rec in tre_recs:
        if tre_rec.treIndex >= treIndex:
            with db.auto_commit():
                tre_rec.treIndex += 1
    data = request.get_json()
    json2db({
        'pid': pid,
        'treNum': len(tre_recs) + 1,
        'treIndex': treIndex,
        'trement': data.get('trement')
    }, TreRec)

    return Success()


@api.route('/<int:pid>/<int:treIndex>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_record_info(pid, treIndex):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    if treIndex > len(tre_recs) or treIndex < 1:
        return ParameterException(msg='treIndex wrong')

    for tre_rec in tre_recs:
        if tre_rec.treIndex > treIndex:
            with db.auto_commit():
                tre_rec.treIndex -= 1
        elif tre_rec.treIndex == treIndex:
            with db.auto_commit():
                tre_rec.delete()

    return Success()
