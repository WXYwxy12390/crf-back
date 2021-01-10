from datetime import timedelta as td, datetime

from flask import request, g,current_app

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, delete_array, db
from app.models.base_line import Patient
from app.models.crf_info import FollInfo
from app.models.cycle import Signs, SideEffect
from app.models.therapy_record import TreRec
from app.spider.research_center import ResearchCenterSpider
from app.utils.date import str2date

api = Redprint('treatment_info')


# 疗效评估的获取和提交
@api.route('/evaluation/<int:pid>/<int:treNum>/<string:trement>', methods=['GET'])
def get_treatment_evaluation(pid, treNum, trement):
    treRec = TreRec.query.filter_by(pid=pid, treNum=treNum, trement=trement).first()
    return Success(data=treRec if treRec else {})


@api.route('/evaluation/<int:pid>/<int:treNum>/<string:trement>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_treatment_evaluation(pid, treNum, trement):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    data['trement'] = trement
    json2db(data, TreRec)
    """
    每一次治疗信息中，疗效评估页面，增加一个字段"PFS/DFS"，该字段可以手动录入，也可以系统自动计算填写，自动计算优先于手动填写。
    当最佳疗效评估选择“PD”且填写了进展时间之后，系统需要自动计算PFS/DFS，并填写，计算逻辑为：用药开始时间到进展时间之间的时间间隔。如果不自动计算，则可以手动填写
    """
    if data.get('beEffEva') == "1" and 'proDate' in data and 'PFS_DFS' not in data:
        treRec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
        treRec.compute_FPS_DFS()
    return Success()


# 症状体征的获取、提交、删除
@api.route('/signs/<int:pid>/<int:treNum>', methods=['GET'])
def get_signs(pid, treNum):
    signs = Signs.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=signs if signs else [])


@api.route('/signs/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_signs(pid, treNum):
    data = request.get_json()
    print(data)
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, Signs)
    return Success()


@api.route('/signs/<int:pid>/<int:sign_id>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_signs(pid,sign_id):
    sign = Signs.query.filter_by(id=sign_id).all()
    delete_array(sign)
    return Success()


# 副反应的获取、提交、删除
@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['GET'])
def get_side_effect(pid, treNum):
    side_effect = SideEffect.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=side_effect if side_effect else [])


@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_side_effect(pid, treNum):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, SideEffect)
    return Success()


@api.route('/side_effect/<int:pid>/<int:se_id>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_side_effect(pid,se_id):
    side_effect = SideEffect.query.filter_by(id=se_id).all()
    delete_array(side_effect)
    return Success()


# 随访信息表的获取、提交、删除
@api.route('/follInfo/<int:pid>', methods=['GET'])
def get_follInfo(pid):
    follInfo = FollInfo.query.filter_by(pid=pid).all()
    return Success(data=follInfo if follInfo else [])


@api.route('/follInfo/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_follInfo(pid):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        json2db(_data, FollInfo)
    return Success()


@api.route('/follInfo/<int:pid>/<int:fid>', methods=['DELETE'])
@auth.login_required
@update_time
def del_follInfo(pid,fid):
    follInfo = FollInfo.query.filter_by(id=fid).all()
    delete_array(follInfo)
    return Success()


# 设置病人随访提醒
@api.route('/patient/follInfo/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_patient_follInfo(pid):
    data = request.get_json()
    data['id'] = pid
    data['finishFollowup'] = 0
    json2db(data, Patient)
    return Success()


# 获得随访提醒表单
@api.route('/patient/follInfo', methods=['GET'])
@auth.login_required
def get_patient_follInfo():
    # id = g.user.user_id
    today = datetime.today().__format__("%Y-%m-%d")
    today = datetime.strptime(today, "%Y-%m-%d")
    tomorrow = today + td(days=3)

    patients = []
    if 'OperateAllCRF' in g.user.scopes:
        patients = Patient.query.filter(Patient.nextFollowupTime >= today, Patient.nextFollowupTime <= tomorrow,Patient.is_delete == 0,Patient.finishFollowup == 0).order_by(Patient.nextFollowupTime.asc()).all()
    elif 'CheckCenterCRF' in g.user.scopes:
        centers = ResearchCenterSpider().search_by_uid_project(current_app.config['PROJECT_ID'], g.user.user_id)['data']
        center_ids = [center['id'] for center in centers]
        patients = Patient.query.filter(Patient.nextFollowupTime >= today, Patient.nextFollowupTime <= tomorrow,Patient.is_delete == 0,Patient.finishFollowup == 0,Patient.researchCenter.in_(center_ids)).order_by(Patient.nextFollowupTime.asc()).all()
    else:
        items = Patient.query.filter(Patient.nextFollowupTime >= today, Patient.nextFollowupTime <= tomorrow,Patient.is_delete == 0,Patient.finishFollowup == 0).order_by(Patient.nextFollowupTime.asc()).all()
        for item in items:
            if item.account and g.user.user_id in item.account:
                patients.append(item)
    # patients = Patient.query.filter(Patient.nextFollowupTime >= today, Patient.nextFollowupTime <= tomorrow,Patient.is_delete == 0,Patient.finishFollowup == 0).order_by(Patient.nextFollowupTime.asc()).all()
    # new_patients = filter(lambda patient: True if patient.account and id in patient.account else False, patients)
    return Success(data=patients if patients else [])


# 关闭随访提醒（完成随访）(通过用户id以及下次随访时间来查询）
@api.route('/patient/follInfo/<int:pid>/<string:nextFollowupTime>', methods=['PUT'])
@auth.login_required
@edit_need_auth
@update_time
def update_patient_follInfo(pid, nextFollowupTime):
    patients = Patient.query.filter_by(id=pid, finishFollowup=0,
                                       nextFollowupTime=datetime.strptime(nextFollowupTime, "%Y-%m-%d")).all()
    with db.auto_commit():
        for patient in patients:
            patient.finishFollowup = 1
    return Success()
