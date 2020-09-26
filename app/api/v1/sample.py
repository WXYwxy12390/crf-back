"""
@author: yours
@file: patient.py
@time: 2020-09-17 15:06
"""

from flask import request, jsonify

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, db, delete_array
from app.models.base_line import Patient
from app.utils.paging import get_paging

api = Redprint('sample')


@api.route('/all',methods=['POST'])
def get_sample_all():
    args = request.args.to_dict()
    data = request.get_json()
    patients = Patient.query.filter_by().all()
    if data and len(data) > 0:
        patients = Patient.search(patients,data)
    res = [patient.get_fotmat_info() for patient in patients]
    res = sorted(res, key=lambda re: re['update_time'], reverse=True)
    res, total = get_paging(res, int(args['page']), int(args['limit']))
    data = {
        "code": 200,
        "msg": "获取样本成功",
        "data": res,
        "total": total
    }
    return jsonify(data)

@api.route('',methods=['POST'])
def add_sample():
    json2db({},Patient)
    return Success()


@api.route('',methods=['DELETE'])
def del_sample():
    data = request.get_json()
    patients = Patient.query.filter(Patient.is_delete==0,Patient.id.in_(data['ids'])).all()
    delete_array(patients)
    return Success()