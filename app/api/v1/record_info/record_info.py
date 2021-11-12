"""
@author: yours
@file: record_info.py
@time: 2020-09-16 20:44
"""
from flask import request
from sqlalchemy import func

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
    tre_recs = TreRec.query.filter(TreRec.pid == pid,
                                   TreRec.is_delete == 0).order_by(TreRec.treIndex).all()
    all_treIndex_treNum = []
    for tre_rec in tre_recs:
        dic = {'treIndex': tre_rec.trement, 'treNum': tre_rec.treNum}
        all_treIndex_treNum.append(dic)
    return Success(data=all_treIndex_treNum)


@api.route('/nav/change/<int:pid>/<int:old>/<int:new>', methods=['GET'])
@auth.login_required
def change_nav_pos(pid, old, new):
    tre_recs = TreRec.query.filter(TreRec.pid == pid,
                                   TreRec.is_delete == 0).order_by(TreRec.treIndex).all()
    length = len(tre_recs)
    if old < 1 or new > length or new < 1 or old > length:
        return ParameterException(msg='位置参数有误')
    if old == new:
        return Success()
    with db.auto_commit():
        if new > old:
            for i in range(old, new):
                tre_recs[i].treIndex -= 1
        else:
            for i in range(new - 1, old - 1):
                tre_recs[i].treIndex += 1
        tre_recs[old - 1].treIndex = new

    return Success()


@api.route('/<int:pid>/<int:treIndex>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_record_info(pid, treIndex):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    max_treNum = 0
    if treIndex > len(tre_recs) + 1 or treIndex < 1:
        return ParameterException(msg='treIndex wrong')
    for tre_rec in tre_recs:
        if tre_rec.treNum > max_treNum:
            max_treNum = tre_rec.treNum
        if tre_rec.treIndex >= treIndex:
            with db.auto_commit():
                tre_rec.treIndex += 1

    data = request.get_json()
    json2db({
        'pid': pid,
        'treNum': max_treNum + 1,
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
    treIndexes_of_tre_recs = [tre_rec.treIndex for tre_rec in tre_recs]
    if treIndex not in treIndexes_of_tre_recs:
        return ParameterException(msg='treIndex wrong')

    for tre_rec in tre_recs:
        if tre_rec.treIndex > treIndex:
            with db.auto_commit():
                tre_rec.treIndex -= 1
        elif tre_rec.treIndex == treIndex:
            with db.auto_commit():
                tre_rec.delete()

    return Success()


@api.route('/max_treIndex', methods=['POST'])
def get_max_treIndex():
    data = request.get_json()
    pids = data.get('pids') if data is not None else None
    if pids:
        res = TreRec.query.filter(TreRec.is_delete == 0,
                                  TreRec.pid.in_(pids)).all()
        max = 0
        for treRec in res:
            max = treRec.treIndex if treRec.treIndex > max else max
    else:
        res = db.session.query(func.max(TreRec.treIndex)).first()
        max = res[0]
    return Success(data=max)
