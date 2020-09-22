"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan

api = Redprint('therapy_record')

@api.route('/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_record(pid,treNum):
    tre_rec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
    data = {}
    if tre_rec :
        one_to_five = OneToFive.query.filter_by(pid=pid,treNum=treNum).first()
        surgery = Surgery.query.filter_by(pid=pid, treNum=treNum).first()
        radiotherapy = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first()
        data['one_to_five'] = one_to_five if one_to_five else {}
        data['surgery'] = surgery if surgery else {}
        data['radiotherapy'] = radiotherapy if radiotherapy else {}
    data['trement'] = tre_rec.trement
    return Success(data=data)


@api.route('/<int:pid>/<int:treNum>',methods=['POST'])
def add_therapy_record(pid,treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    tre_rec_data = {

    }
    json2db(data, TreRec)
    trement = data['parent']['trement']
    if data[''] in ['one','two','three','four','five']:
        json2db(data,OneToFive)
    elif data['trement'] == 'surgery':
        json2db(data, Surgery)
    elif data['trement'] == 'radiotherapy':
        json2db(data, Radiotherapy)


    return Success(data=data)



@api.route('/therapy_plan/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_plan(pid,treNum):
    args = request.args.to_dict()
    treSolu = args['treSolu']
    items = DetailTrePlan.query.filter_by(pid=pid,treNum=treNum,treSolu=treSolu).all()
    return Success(data=items if items else [])


