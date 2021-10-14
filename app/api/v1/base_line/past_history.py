"""
@author: yours
@file: past_history.py
@time: 2020-09-04 21:03
"""

from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db
from app.models.base_line import PastHis, Patient, DrugHistory
from app.utils.modification import record_modification, if_status_allow_modification

api = Redprint('past_history')


@api.route('/<int:pid>', methods=['GET'])
def get_past_history(pid):
    past_history = PastHis.query.filter_by(pid=pid).first()
    return Success(data=past_history if past_history else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_past_history(pid):
    data = request.get_json()
    data["pid"] = pid

    item = PastHis.query.filter_by(pid=pid).first()
    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, 0, 'PastHis'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, 0, 'PastHis', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    json2db(data, PastHis)
    return Success()


# @api.route('/doubt/<int:pid>', methods=['POST'])
# @auth.login_required
# def doubt_past_history(pid):
#     data = request.get_json()
#     item = PastHis.query.filter_by(pid=pid).first_or_404()
#     if item.question(data, pid, 0):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/reply/<int:pid>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_past_history(pid, doubt_index):
#     data = request.get_json()
#     item = PastHis.query.filter_by(pid=pid).first_or_404()
#     if item.reply_doubt(data, pid, 0, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


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
def add_drug_history(pid):
    data = request.get_json()
    data["pid"] = pid

    id = data.get('id')
    item = DrugHistory.query.get_or_404(id) if id is not None else None
    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, 0, 'DrugHistory'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, 0, 'DrugHistory', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

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


# @api.route('/drug_history/doubt/<int:drug_history_id>', methods=['POST'])
# @auth.login_required
# def doubt_drug_history(drug_history_id):
#     data = request.get_json()
#     item = DrugHistory.query.get_or_404(drug_history_id)
#     if item.question(data, item.pid, 0):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/drug_history/reply/<int:drug_history_id>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_drug_history(drug_history_id, doubt_index):
#     data = request.get_json()
#     item = DrugHistory.query.get_or_404(drug_history_id)
#     if item.reply_doubt(data, item.pid, 0, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


