"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan

api = Redprint('therapy_record')

@api.route('/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_record(pid,treNum):
    tre_rec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
    data = {}
    if tre_rec :
        if tre_rec.trement in ['one','two','three','four','five']:
            data = OneToFive.query.filter_by(pid=pid,treNum=treNum).first()
        elif tre_rec.trement == 'surgery':
            data = Surgery.query.filter_by(pid=pid,treNum=treNum).first()
        elif tre_rec.trement == 'radiotherapy':
            data = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=data)

@api.route('/<int:pid>/<int:treNum>',methods=['POST'])
def add_therapy_record(pid,treNum):
    data = request.get_json()

    return Success(data=data)

@api.route('/therapy_plan/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_plan(pid,treNum):
    args = request.args.to_dict()
    treSolu = args['treSolu']
    items = DetailTrePlan.query.filter_by(pid=pid,treNum=treNum,treSolu=treSolu).all()
    return Success(data=items if items else [])


