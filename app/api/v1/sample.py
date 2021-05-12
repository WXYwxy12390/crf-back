"""
@author: yours
@file: patient.py
@time: 2020-09-17 15:06
"""

from flask import request, jsonify, g, current_app
from sqlalchemy import func

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.error_code import PostError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array, json2db_add
from app.models.base_line import Patient
from app.spider.research_center import ResearchCenterSpider
from app.spider.user_info import UserInfo
from app.utils.export import Export
from app.utils.paging import get_paging

api = Redprint('sample')


@api.route('/all', methods=['POST'])
@auth.login_required
def get_sample_all():
    args = request.args.to_dict()
    data = request.get_json()
    page = int(args['page'])
    limit = int(args['limit'])
    patients = []
    if 'OperateAllCRF' in g.user.scopes:
        patients = Patient.query.filter_by().order_by(Patient.update_time.desc()).all()
    elif 'CheckCenterCRF' in g.user.scopes:
        centers = ResearchCenterSpider().search_by_uid_project(current_app.config['PROJECT_ID'], g.user.user_id)['data']
        center_ids = [center['id'] for center in centers]
        patients = Patient.query.filter(Patient.is_delete == 0, Patient.researchCenter.in_(center_ids)
                                        ).order_by(Patient.update_time.desc()).all()
    else:
        items = Patient.query.filter(Patient.is_delete == 0).order_by(Patient.update_time.desc()).all()
        for item in items:
            if item.account and g.user.user_id in item.account:
                patients.append(item)
    all_pids = [patient.id for patient in patients]
    if data and len(data) > 0:
        res, total, all_pids = Patient.search(patients, data, page, limit)
    else:
        res, total = get_paging(patients, page, limit)
    res = [patient.get_fotmat_info() for patient in res]
    data = {
        "code": 200,
        "msg": "获取样本成功",
        "data": res,
        "total": total,
        "all_pids": all_pids
    }
    return jsonify(data)


@api.route('/updated', methods=['GET','POST'])
@auth.login_required
def get_sample_updated():
    args = request.args.to_dict()
    page = int(args['page'])
    limit = int(args['limit'])
    all_patients = []
    updated_patients = []
    if 'OperateAllCRF' in g.user.scopes:
        all_patients = Patient.query.filter_by().order_by(Patient.update_time.desc()).all()
    elif 'CheckCenterCRF' in g.user.scopes:
        centers = ResearchCenterSpider().search_by_uid_project(current_app.config['PROJECT_ID'], g.user.user_id)['data']
        center_ids = [center['id'] for center in centers]
        all_patients = Patient.query.filter(Patient.is_delete == 0, Patient.researchCenter.in_(center_ids)
                                        ).order_by(Patient.update_time.desc()).all()
    else:
        items = Patient.query.filter(Patient.is_delete == 0).order_by(Patient.update_time.desc()).all()
        for item in items:
            if item.account and g.user.user_id in item.account:
                all_patients.append(item)

    for patient in all_patients:
        if patient.create_time == patient.update_time:
            updated_patients.append(patient)
    pids = [patient.id for patient in updated_patients]
    res, total = get_paging(updated_patients, page, limit)
    res = [patient.get_fotmat_info() for patient in res]
    data = {
        "code": 200,
        "msg": "获取样本成功",
        "data": res,
        "total": total,
        "all_pids": pids
    }
    return jsonify(data)


# 新增样本
@api.route('', methods=['POST'])
@auth.login_required
def add_sample():
    data = request.get_json()
    user = UserInfo().search_by_uid(g.user.user_id)['data']
    patients = None
    if 'idNumber' in data:
        patients = Patient.query.filter_by(idNumber=data['idNumber'], researchCenter=user['research_center_id']).all()
    if 'hospitalNumber' in data:
        patients = Patient.query.filter_by(hospitalNumber=data['hospitalNumber'],
                                           researchCenter=user['research_center_id']).all()
    if 'patientName' in data:
        patients = Patient.query.filter_by(patientName=data['patientName'],
                                           researchCenter=user['research_center_id']).all()
    return_data = {
        "status": 0,
        "pid": None,
        "samples": []
    }
    if patients:
        return_data['status'] = 1
        for patient in patients:
            return_data['samples'].append(patient)
            if g.user.user_id in patient.account:
                return_data['status'] = -1
        return Success(data=return_data)

    model_data = {
        'account': [user['id']],
        'researchCenter': user['research_center_id'],
        'idNumber': data.get('idNumber'),
        'hospitalNumber': data.get('hospitalNumber'),
        'patientName': data.get('patientName'),
        'birthday': data.get('birthday')
    }
    patient = json2db_add(model_data, Patient)
    return_data['pid'] = patient.id
    return Success(data=return_data)


@api.route('/<int:pid>/add_account', methods=['POST'])
@auth.login_required
def sample_add_account(pid):
    patient = Patient.query.get_or_404(pid)
    with db.auto_commit():
        account = [id for id in patient.account]
        account.append(g.user.user_id)
        patient.account = list(set(account))

    return Success()


@api.route('', methods=['DELETE'])
@auth.login_required
def del_sample():
    data = request.get_json()
    patients = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(data['ids'])).all()
    delete_array(patients)
    return Success()


@api.route('/export', methods=['POST'])
def export():
    data = request.get_json()
    pids = data.get('pids')
    return Export(pids).work()
