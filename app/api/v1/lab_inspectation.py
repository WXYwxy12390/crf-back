"""
@author: yours
@file: lab_inspectation.py
@time: 2020-09-05 12:30
"""
from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db
from app.models.lab_inspectation import BloodRoutine

api = Redprint('lab_inspectation')

@api.route('/blood_routine/<int:pid>/<int:treNum>',methods=['GET'])
def get_blood_routine(pid,treNum):
    blood_routine = BloodRoutine.query.filter_by(pid=pid,treNum=treNum).first()
    return Success(data=blood_routine if blood_routine else {})


@api.route('/blood_routine/<int:pid>/<int:treNum>',methods=['POST'])
def add_blood_routine(pid,treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, BloodRoutine)
    return Success()


