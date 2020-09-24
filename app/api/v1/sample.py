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


@api.route('/all',methods=['GET'])
def get_sample_all():
    args = request.args.to_dict()
    patients = Patient.query.filter_by().all()
    res = [patient.get_fotmat_info() for patient in patients]
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


