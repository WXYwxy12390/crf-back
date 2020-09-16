"""
@author: yours
@file: record_info.py
@time: 2020-09-16 20:44
"""
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models.therapy_record import TreRec

api = Redprint('record_info')

@api.route('/nav/<int:pid>',methods = ['GET'])
def get_record_info_nav(pid):
    tre_recs = TreRec.query.filter_by(pid=pid).all()
    return Success(data=len(tre_recs))