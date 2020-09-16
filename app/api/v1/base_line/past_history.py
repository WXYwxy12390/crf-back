"""
@author: yours
@file: past_history.py
@time: 2020-09-04 21:03
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, db
from app.models.base_line import PastHis, Patient, DrugHistory

api = Redprint('past_history')

@api.route('/<int:pid>',methods = ['GET'])
def get_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first()
    return Success(data=past_history if past_history else {})


@api.route('/<int:pid>',methods = ['POST'])
def add_past_history(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
    data["pid"] = patient.id
    json2db(data, PastHis)
    return Success()

@api.route('/drug_history/<int:pid>',methods=['GET'])
def get_drug_history(pid):
    args = request.args.to_dict()
    type = int(args['type'])
    drugs = DrugHistory.query.filter_by(pid=pid,type=type).all()
    return Success(data= drugs if drugs else [])

@api.route('/drug_history/<int:pid>',methods=['POST'])
def add_drug_history(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
    data["pid"] = patient.id
    json2db(data, DrugHistory)
    return Success()

@api.route('/drug_history/<int:pid>',methods=['DELETE'])
def del_hormone_history(pid):
    data = request.get_json()
    items = DrugHistory.query.filter(DrugHistory.is_delete==0,DrugHistory.id.in_(data['ids'])).all()
    with db.auto_commit():
        for item in items:
            item.delete()
    return Success()