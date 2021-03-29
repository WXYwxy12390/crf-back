"""
@author: yours
@file: record_info.py
@time: 2020-09-16 20:44
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, json2db_add
from app.models.therapy_record import TreRec

api = Redprint('record_info')

@api.route('/nav/<int:pid>',methods = ['GET'])
def get_record_info_nav(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    return Success(data=len(tre_recs))

@api.route('/<int:pid>',methods = ['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_record_info(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    data = request.get_json()
    json2db({
        'pid':pid,
        'treNum':len(tre_recs) + 1,
        'trement': data.get('trement')
    },TreRec)



    return Success()

@api.route('/<int:pid>',methods = ['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_record_info(pid):
    tre_rec = TreRec.query.filter_by(pid=pid).order_by(TreRec.treNum.desc()).first()
    if tre_rec:
        with db.auto_commit():
            tre_rec.delete()
    return Success()