"""
@author: yours
@file: first_diagnose.py
@time: 2020-09-14 21:26
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time, record_modification
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
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
# @record_modification(IniDiaPro)
def add_first_diagnose(pid):
    data = request.get_json()
    data["pid"] = pid
    json2db(data, IniDiaPro)
    return Success()


@api.route('/submit/<int:pid>', methods=['GET'])
@auth.login_required
def submit_first_diagnose(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module('IniDiaPro', 0):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/begin_monitor/<int:pid>', methods=['GET'])
@auth.login_required
def begin_monitor_first_diagnose(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor('IniDiaPro', 0):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/finish/<int:pid>', methods=['GET'])
@auth.login_required
def finish_first_diagnose(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.finish('IniDiaPro', 0):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


@api.route('/doubt/<int:pid>', methods=['POST'])
@auth.login_required
def doubt_first_diagnose(pid):
    data = request.get_json()
    item = IniDiaPro.query.filter_by(pid=pid).first_or_404()
    if item.question(data, pid, 0):
        return Success()
    else:
        return SampleStatusError()


@api.route('/reply/<int:pid>/<int:doubt_index>', methods=['POST'])
@auth.login_required
def reply_first_diagnose(pid, doubt_index):
    data = request.get_json()
    item = IniDiaPro.query.filter_by(pid=pid).first_or_404()
    if item.reply_doubt(data, pid, 0, doubt_index):
        return Success()
    else:
        return SampleStatusError()
