"""
@author: yours
@file: patient.py
@time: 2020-09-17 15:06
"""
import copy

from flask import request, jsonify, g, current_app

from app.config.secure import fudan_zhongliu_research_center_id, fudan_zhongshan_research_center_id, ARION_research_id
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array, json2db_add
from app.models.base_line import Patient
from app.models.researchPatient import ResearchPatient
from app.spider.research_center import ResearchCenterSpider
from app.spider.user_info import UserInfo
from app.utils.paging import get_paging
from app.utils.sort import sort_samples_while_query

api = Redprint('sample')


@api.route('/all', methods=['POST'])
@auth.login_required
def get_sample_all():
    args = request.args.to_dict()
    data = request.get_json()
    page = int(args['page'])
    limit = int(args['limit'])
    sort = int(args.get('sort')) if args.get('sort') else None
    patients = []
    if 'OperateAllCRF' in g.user.scopes:
        patients = sort_samples_while_query(Patient.query.filter_by(), sort)

    elif 'CheckCenterCRF' in g.user.scopes:
        centers = ResearchCenterSpider().search_by_uid_project(current_app.config['PROJECT_ID'], g.user.user_id)['data']
        center_ids = [center['id'] for center in centers]
        patients = sort_samples_while_query(Patient.query.filter(Patient.is_delete == 0,
                                                                 Patient.researchCenter.in_(center_ids)), sort)
    elif 'CheckAllInResearch' in g.user.scopes:
        all_research_patient = ResearchPatient.query.filter_by().all()
        pids_in_all_research = [research_patient.pid for research_patient in all_research_patient]
        patients = sort_samples_while_query(Patient.query.filter(Patient.is_delete == 0,
                                                                 Patient.id.in_(pids_in_all_research)), sort)
    elif 'CheckCenterInResearch' in g.user.scopes:
        centers = ResearchCenterSpider().search_by_uid_project(current_app.config['PROJECT_ID'], g.user.user_id)['data']
        center_ids = [center['id'] for center in centers]
        all_research_patient = ResearchPatient.query.filter_by().all()
        pids_in_all_research = [research_patient.pid for research_patient in all_research_patient]
        patients = sort_samples_while_query(Patient.query.filter(Patient.is_delete == 0,
                                                                 Patient.id.in_(pids_in_all_research),
                                                                 Patient.researchCenter.in_(center_ids)), sort)
    else:
        items = sort_samples_while_query(Patient.query.filter(Patient.is_delete == 0), sort)
        for item in items:
            if item.account and g.user.user_id in item.account:
                patients.append(item)

    all_pids = [patient.id for patient in patients]
    if data and len(data) > 0:
        res, total, all_pids = Patient.search(patients, data, page, limit, sort)
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


@api.route('/unchanged', methods=['GET', 'POST'])
@auth.login_required
def get_sample_updated():
    args = request.args.to_dict()
    page = int(args['page']) if args.get('page') else 1
    limit = int(args['limit']) if args.get('limit') else 10
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

    if (not args.get('page')) and (not args.get('limit')):
        page = 1
        limit = len(updated_patients)
    patient_list, total = get_paging(updated_patients, page, limit)
    patient_list = [patient.get_fotmat_info() for patient in patient_list]
    data = {
        "total": total,
        "patients": patient_list
    }
    res = {
        "code": 200,
        "msg": "获取样本成功",
        "data": data
    }
    return jsonify(res)


# 新增样本
@api.route('', methods=['POST'])
@auth.login_required
def add_sample():
    data = request.get_json()
    user = UserInfo().search_by_uid(g.user.user_id)['data']
    id_patients = None
    hos_patients = None
    name_patients = None
    if 'idNumber' in data:
        id_patients = Patient.query.filter_by(idNumber=data['idNumber'],
                                              researchCenter=user['research_center_id']).all()
    if 'hospitalNumber' in data:
        hos_patients = Patient.query.filter_by(hospitalNumber=data['hospitalNumber'],
                                               researchCenter=user['research_center_id']).all()
    if 'patientName' in data:
        name_patients = Patient.query.filter_by(patientName=data['patientName'],
                                                researchCenter=user['research_center_id']).all()
    # status值的含义
    # 0表示该样本不存在，直接添加
    # 1表示该样本存在，但是不由当前账号录入
    # -1表示该样本存在，由当前账号录入，让用户选择是否直接进入
    # 2表示该样本存在，让用户选择是新建还是进入
    return_data = {
        "status": 0,
        "pid": None,
        "samples": []
    }
    if id_patients:
        return_data['status'] = 1
        for patient in id_patients:
            return_data['samples'].append(patient)
            if g.user.user_id in patient.account:
                return_data['status'] = -1
        return Success(data=return_data)
    elif hos_patients:
        return_data['status'] = 1
        for patient in hos_patients:
            return_data['samples'].append(patient)
            if g.user.user_id in patient.account:
                return_data['status'] = -1
        return Success(data=return_data)
    # 当请求中有"if_create"表示新建一个同名样本；没有"if_create"则不新建
    elif name_patients and 'if_create' not in data:
        return_data['status'] = 2
        for patient in name_patients:
            return_data['samples'].append(patient)
        return Success(data=return_data)

    model_data = {
        'account': [user['id']],
        'researchCenter': user['research_center_id'],
        'idNumber': data.get('idNumber'),
        'hospitalNumber': data.get('hospitalNumber'),
        'patientName': data.get('patientName'),
        'birthday': data.get('birthday'),
        'phoneNumber1': data.get('phoneNumber1'),
        'patNumber': data.get('patNumber')
    }
    patient = json2db_add(model_data, Patient)
    return_data['pid'] = patient.id
    # 复旦肿瘤和复旦中山两个中心的主任、录入员录入病人后，病人自动被移入ARION研究
    if user['research_center_id'] in [fudan_zhongliu_research_center_id, fudan_zhongshan_research_center_id] and \
            'OperatePatientsInResearch' in g.user.scopes:
        json2db_add({'pid': patient.id, 'rid': ARION_research_id, 'uid': user['id']}, ResearchPatient)
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
    scopes = g.user.scopes
    uid = g.user.user_id
    data = request.get_json()
    pids = data['ids']
    patients = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).all()
    if 'OperateAllCRF' in scopes or 'EditCenterCRF' in scopes or 'CheckCenterCRF' in scopes:
        delete_array(patients)
    elif 'OperateUserCRF' in scopes:
        for patient in patients:
            if uid in patient.account:
                account = copy.copy(patient.account)
                account.remove(uid)
                with db.auto_commit():
                    patient.account = account
    return Success()
