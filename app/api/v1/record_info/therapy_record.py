"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, delete_array
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan

api = Redprint('therapy_record')

@api.route('/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_record(pid,treNum):
    tre_rec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
    data = {}
    if tre_rec :
        data['parent'] = tre_rec.get_parent()
        data['child'] = tre_rec.get_child()
    return Success(data=data)


@api.route('/<int:pid>/<int:treNum>',methods=['POST'])
def add_therapy_record(pid,treNum):
    data = request.get_json()
    if 'parent' in data:
        data['parent']['pid'] = pid
        data['parent']['treNum'] = treNum
        json2db(data['parent'], TreRec)
    if 'child' in data:
        tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
        trement = tre_rec.trement
        data['child']['pid'] = pid
        data['child']['treNum'] = treNum
        if trement in ['one','two','three','four','five','other']:
            json2db(data['child'],OneToFive)
        elif trement == 'surgery':
            json2db(data['child'], Surgery)
        elif trement == 'radiotherapy':
            json2db(data['child'], Radiotherapy)
    return Success()



@api.route('/therapy_plan/<int:pid>/<int:treNum>',methods=['GET'])
def get_therapy_plan(pid,treNum):
    items = DetailTrePlan.query.filter_by(pid=pid,treNum=treNum).all()
    data = {}
    data['Chemotherapy'] ,data['TargetedTherapy'],data['ImmunityTherapy'],data['AntivascularTherapy']= [],[],[],[]
    for item in items:
        if item.treSolu:
            data[item.treSolu].append(item)

    return Success(data=data)


@api.route('/therapy_plan/<int:pid>/<int:treNum>',methods=['POST'])
def add_therapy_plan(pid,treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data,DetailTrePlan)
    return Success()


@api.route('/therapy_plan/<int:pid>/<int:treNum>',methods=['DELETE'])
def del_therapy_plan(pid,treNum):
    data = request.get_json()
    items = DetailTrePlan.query.filter(DetailTrePlan.is_delete==0,DetailTrePlan.id.in_(data['ids'])).all()
    delete_array(items)

    return Success()