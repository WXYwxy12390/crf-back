"""
@author: yours
@file: record_info.py
@time: 2020-09-16 20:44
"""
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, db
from app.models.therapy_record import TreRec

api = Redprint('record_info')

@api.route('/nav/<int:pid>',methods = ['GET'])
def get_record_info_nav(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    return Success(data=len(tre_recs))

@api.route('/<int:pid>',methods = ['POST'])
def add_record_info(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    json2db({
        'pid':pid,
        'treNum':len(tre_recs) + 1
    },TreRec)
    return Success()

@api.route('/<int:pid>',methods = ['DELETE'])
def del_record_info(pid):
    tre_rec = TreRec.query.filter_by(pid=pid).order_by(TreRec.treNum.desc()).first()
    if tre_rec:
        with db.auto_commit():
            tre_rec.delete()
    return Success()