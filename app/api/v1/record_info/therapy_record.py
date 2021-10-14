"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""
from flask import request
from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, delete_array
from app.models.base_line import Patient
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan
from app.utils.modification import record_modification, if_status_allow_modification

api = Redprint('therapy_record')


@api.route('/<int:pid>/<int:treNum>', methods=['GET'])
def get_therapy_record(pid, treNum):
    tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first()
    data = {}
    if tre_rec:
        data['parent'] = tre_rec.get_parent()
        data['child'] = tre_rec.get_child()
    return Success(data=data)


@api.route('/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_therapy_record(pid, treNum):
    data = request.get_json()
    if 'parent' in data:
        data['parent']['pid'] = pid
        data['parent']['treNum'] = treNum
        data['parent']['is_auto_compute'] = 1
        json2db(data['parent'], TreRec)
    if 'child' in data:
        tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
        trement = tre_rec.trement
        data['child']['pid'] = pid
        data['child']['treNum'] = treNum
        if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
            item = OneToFive.query.filter_by(pid=pid, treNum=treNum).first()
            # 当存在'modification_des'时，说明需要记录下该修改。
            if 'modification_des' in data.keys():
                if not record_modification(item, data, pid, treNum, 'OneToFive'):
                    return SampleStatusError(msg='当前模块状态无法修改数据')
            else:
                if not if_status_allow_modification(pid, treNum, 'OneToFive', False):
                    return SampleStatusError(msg='当前模块状态无法修改数据')

            json2db(data['child'], OneToFive)
        elif trement == 'surgery':
            item = Surgery.query.filter_by(pid=pid, treNum=treNum).first()
            # 当存在'modification_des'时，说明需要记录下该修改。
            if 'modification_des' in data.keys():
                if not record_modification(item, data, pid, treNum, 'Surgery'):
                    return SampleStatusError(msg='当前模块状态无法修改数据')
            else:
                if not if_status_allow_modification(pid, treNum, 'Surgery', False):
                    return SampleStatusError(msg='当前模块状态无法修改数据')

            json2db(data['child'], Surgery)
        elif trement == 'radiotherapy':
            item = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first()
            # 当存在'modification_des'时，说明需要记录下该修改。
            if 'modification_des' in data.keys():
                if not record_modification(item, data, pid, treNum, 'Radiotherapy'):
                    return SampleStatusError(msg='当前模块状态无法修改数据')
            else:
                if not if_status_allow_modification(pid, treNum, 'Radiotherapy', False):
                    return SampleStatusError(msg='当前模块状态无法修改数据')

            json2db(data['child'], Radiotherapy)
    return Success()


# @api.route('/doubt/<int:pid>/<int:treNum>', methods=['POST'])
# @auth.login_required
# def doubt_therapy_record(pid, treNum):
#     tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     trement = tre_rec.trement
#     if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
#         item = OneToFive.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     elif trement == 'surgery':
#         item = Surgery.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     elif trement == 'radiotherapy':
#         item = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#
#     data = request.get_json()
#     if item.question(data, item.pid, item.treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/reply/<int:pid>/<int:treNum>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_therapy_record(pid, treNum, doubt_index):
#     data = request.get_json()
#     tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     trement = tre_rec.trement
#     if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
#         item = OneToFive.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     elif trement == 'surgery':
#         item = Surgery.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     elif trement == 'radiotherapy':
#         item = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#
#     if item.reply_doubt(data, pid, treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


@api.route('/therapy_plan/<int:pid>/<int:treNum>', methods=['GET'])
def get_therapy_plan(pid, treNum):
    items = DetailTrePlan.query.filter_by(pid=pid, treNum=treNum).all()
    data = {}
    data['Chemotherapy'], data['TargetedTherapy'], data['ImmunityTherapy'], data['AntivascularTherapy'] = [], [], [], []
    for item in items:
        if item.treSolu:
            data[item.treSolu].append(item)

    return Success(data=data)


@api.route('/therapy_plan/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_therapy_plan(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum

    id = data.get('id')
    item = DetailTrePlan.query.get_or_404(id) if id is not None else None
    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, 0, 'DetailTrePlan'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, 0, 'DetailTrePlan', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    json2db(data, DetailTrePlan)
    return Success()


@api.route('/therapy_plan/<int:pid>/<int:treNum>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_therapy_plan(pid, treNum):
    data = request.get_json()
    items = DetailTrePlan.query.filter(DetailTrePlan.is_delete == 0, DetailTrePlan.id.in_(data['ids'])).all()
    delete_array(items)
    return Success()


# @api.route('/therapy_plan/doubt/<int:therapy_plan_id>', methods=['POST'])
# @auth.login_required
# def doubt_therapy_plan(therapy_plan_id):
#     data = request.get_json()
#     item = DetailTrePlan.query.get_or_404(therapy_plan_id)
#     if item.question(data, item.pid, item.treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/therapy_plan/reply/<int:therapy_plan_id>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_therapy_plan(therapy_plan_id, doubt_index):
#     data = request.get_json()
#     item = DetailTrePlan.query.get_or_404(therapy_plan_id)
#     if item.reply_doubt(data, item.pid, item.treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()
