"""
@author: yours
@file: past_history.py
@time: 2020-09-04 21:03
"""

from flask import request

from app.libs.decorator import edit_need_auth, update_time, record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db
from app.models.base_line import PastHis, Patient, DrugHistory

api = Redprint('past_history')


@api.route('/<int:pid>', methods=['GET'])
def get_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first()
    return Success(data=past_history if past_history else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(PastHis)
def add_past_history(pid):
    data = request.get_json()
    data["pid"] = pid
    json2db(data, PastHis)
    return Success()


@api.route('/submit/<int:pid>', methods=['GET'])
@auth.login_required
def submit_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first_or_404()
    if not past_history.submit():
        return SampleStatusError('当前状态无法提交')

    drug_history_ls = DrugHistory.query.filter_by(pid=pid).all()
    for drug_history in drug_history_ls:
        if drug_history.module_status != ModuleStatus.UnSubmitted.value:
            return SampleStatusError('当前状态无法提交')
    for drug_history in drug_history_ls:
        drug_history.submit()

    return Success(msg='提交成功')


@api.route('/finish/<int:pid>', methods=['GET'])
@auth.login_required
def finish_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first_or_404()
    if not past_history.finish():
        return SampleStatusError('当前状态无法结束监察')

    drug_history_ls = DrugHistory.query.filter_by(pid=pid).all()
    for drug_history in drug_history_ls:
        if drug_history.module_status != ModuleStatus.Submitted.value:
            return SampleStatusError('当前状态无法结束监察')
    for drug_history in drug_history_ls:
        drug_history.finish()

    return Success(msg='监察结束')


@api.route('/doubt/<int:pid>', methods=['POST'])
@auth.login_required
def doubt_past_history(pid):
    data = request.get_json()
    item = PastHis.query.filter_by(pid=pid).first_or_404()

    if item.question(data):
        return Success()
    else:
        return SampleStatusError()


@api.route('/reply/<int:pid>/<int:doubt_id>', methods=['POST'])
@auth.login_required
def reply_past_history(pid, doubt_id):
    data = request.get_json()
    item = PastHis.query.filter_by(pid=pid).first_or_404()
    if item.reply_doubt(doubt_id, data):
        return Success()
    else:
        return SampleStatusError()


@api.route('/drug_history/<int:pid>', methods=['GET'])
def get_drug_history(pid):
    args = request.args.to_dict()
    type = int(args['type'])
    drugs = DrugHistory.query.filter_by(pid=pid, type=type).all()
    return Success(data=drugs if drugs else [])


@api.route('/drug_history/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(DrugHistory)
def add_drug_history(pid):
    data = request.get_json()
    drugHistory = DrugHistory.query.filter_by(pid=pid).first()
    data['module_status'] = drugHistory.module_status if drugHistory else 0
    data["pid"] = pid
    json2db(data, DrugHistory)
    return Success()


@api.route('/drug_history/<int:pid>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_hormone_history(pid):
    data = request.get_json()
    items = DrugHistory.query.filter(DrugHistory.is_delete == 0, DrugHistory.id.in_(data['ids'])).all()
    with db.auto_commit():
        for item in items:
            item.delete()
    return Success()


@api.route('/drug_history/doubt/<int:drug_history_id>', methods=['POST'])
@auth.login_required
def doubt_drug_history(drug_history_id):
    data = request.get_json()
    item = DrugHistory.query.get_or_404(drug_history_id)
    if item.question(data):
        return Success()
    else:
        return SampleStatusError()


@api.route('/drug_history/reply/<int:drug_history_id>/<int:doubt_id>', methods=['POST'])
@auth.login_required
def reply_drug_history(drug_history_id, doubt_id):
    data = request.get_json()
    item = DrugHistory.query.get_or_404(drug_history_id)
    if item.reply_doubt(doubt_id, data):
        return Success()
    else:
        return SampleStatusError()


