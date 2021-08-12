"""
@author: yours
@file: first_diagnose.py
@time: 2020-09-14 21:26
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.base_line import IniDiaPro, Patient

api = Redprint('first_diagnose')


@api.route('/<int:pid>', methods=['GET'])
def get_first_diagnose(pid):
    first_diagnose = IniDiaPro.query.filter_by(pid=pid).first()
    return Success(data=first_diagnose if first_diagnose else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_first_diagnose(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
    data["pid"] = patient.id
    json2db(data, IniDiaPro)
    return Success()
