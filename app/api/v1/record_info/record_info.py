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
    tre_recs = TreRec.query.filter(TreRec.pid == pid,
                                   TreRec.is_delete == 0).order_by(TreRec.treIndex).all()
    all_treIndex_treNum = []
    for tre_rec in tre_recs:
        dic = {'treIndex': tre_rec.treIndex, 'treNum': tre_rec.treNum}
        all_treIndex_treNum.append(dic)
    return Success(data=all_treIndex_treNum)


@api.route('/<int:pid>/<int:treIndex>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_record_info(pid, treIndex):
    tre_recs = TreRec.query.filter(TreRec.pid == pid,
                                   TreRec.is_delete == 0).order_by(TreRec.treIndex).all()
    max_treNum = 0
    max_treIndex = tre_recs[-1].treIndex if tre_recs else 0
    if treIndex < 1 or treIndex > max_treIndex + 1:
        return ParameterException(msg='treIndex wrong')
    for tre_rec in tre_recs:
        if tre_rec.treNum > max_treNum:
            max_treNum = tre_rec.treNum

    begin = 0  # 第二层循环的起始位置
    flag = True  # 当不再有旧的治疗信息更改序号时，第一层循环结束
    for i in range(treIndex, max_treIndex + 1):
        if flag:
            for j in range(begin, len(tre_recs)):
                flag = False
                if tre_recs[j].treIndex == i:
                    begin = j + 1
                    flag = True
                    with db.auto_commit():
                        tre_recs[j].treIndex += 1
                    break
        else:
            break
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
        if tre_rec.treIndex == treIndex:
            with db.auto_commit():
                tre_rec.delete()
            break

    return Success()
