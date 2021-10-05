"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""

from flask import request

from app.libs.decorator import edit_need_auth, update_time, record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, delete_array
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan

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
@record_modification('trement')  # 由于不确定是OneToFive、Surgery还是Radiotherapy，先传trement字符串标识，到装饰器中再单独做处理
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
            json2db(data['child'], OneToFive)
        elif trement == 'surgery':
            json2db(data['child'], Surgery)
        elif trement == 'radiotherapy':
            json2db(data['child'], Radiotherapy)
    return Success()


@api.route('/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_therapy_record(pid, treNum):
    tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    trement = tre_rec.trement
    if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
        trement = OneToFive.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    elif trement == 'surgery':
        trement = Surgery.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    elif trement == 'radiotherapy':
        trement = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if not trement.submit():
        return SampleStatusError('当前状态无法提交')

    detail_tre_plans = DetailTrePlan.query.filter_by(pid=pid, treNum=treNum).all()
    for detail_tre_plan in detail_tre_plans:
        if detail_tre_plan.module_status != ModuleStatus.UnSubmitted.value:
            return SampleStatusError('当前状态无法提交')
    for detail_tre_plan in detail_tre_plans:
        detail_tre_plan.submit()

    return Success(msg='提交成功')


@api.route('/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_therapy_record(pid, treNum):
    tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    trement = tre_rec.trement
    if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
        trement = OneToFive.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    elif trement == 'surgery':
        trement = Surgery.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    elif trement == 'radiotherapy':
        trement = Radiotherapy.query.filter_by(pid=pid, treNum=treNum).first_or_404()

    if not trement.finish():
        return SampleStatusError('当前状态无法结束监察')

    detail_tre_plans = DetailTrePlan.query.filter_by(pid=pid, treNum=treNum).all()
    for detail_tre_plan in detail_tre_plans:
        if detail_tre_plan.module_status != ModuleStatus.Submitted.value:
            return SampleStatusError('当前状态无法结束监察')
    for detail_tre_plan in detail_tre_plans:
        detail_tre_plan.finish()

    return Success(msg='监察结束')


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
@record_modification(DetailTrePlan)
def add_therapy_plan(pid, treNum):
    data = request.get_json()
    detailTrePlan = DetailTrePlan.query.filter_by(pid=pid, treNum=treNum).first()
    data['module_status'] = detailTrePlan.module_status if detailTrePlan else 0
    data['pid'] = pid
    data['treNum'] = treNum
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
