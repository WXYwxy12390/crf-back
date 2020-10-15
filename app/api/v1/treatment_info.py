from datetime import datetime

from flask import request

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, delete_array, db
from app.models.base_line import Patient
from app.models.crf_info import FollInfo
from app.models.cycle import Signs, SideEffect
from app.models.therapy_record import TreRec
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
def add_treatment_evaluation(pid, treNum, trement):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    data['trement'] = trement
    json2db(data, TreRec)
    return Success()


# 症状体征的获取、提交、删除
@api.route('/signs/<int:pid>/<int:treNum>', methods=['GET'])
def get_signs(pid, treNum):
    signs = Signs.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=signs if signs else [])


@api.route('/signs/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_signs(pid, treNum):
    data = request.get_json()
    print(data)
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, Signs)
    return Success()


@api.route('/signs/<int:sign_id>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
def del_signs(sign_id):
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
def add_side_effect(pid, treNum):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, SideEffect)
    return Success()


@api.route('/side_effect/<int:se_id>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
def del_side_effect(se_id):
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
def add_follInfo(pid):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        json2db(_data, FollInfo)
    return Success()


@api.route('/follInfo/<int:fid>', methods=['DELETE'])
@auth.login_required
def del_follInfo(fid):
    follInfo = FollInfo.query.filter_by(id=fid).all()
    delete_array(follInfo)
    return Success()


# 设置病人随访提醒
@api.route('/patient/follInfo/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_patient_follInfo(pid):
    data = request.get_json()
    data['id'] = pid
    data['finishFollowup'] = 0
    json2db(data, Patient)
    return Success()


# 获得随访提醒表单
@api.route('/patient/follInfo', methods=['GET'])
def get_patient_follInfo():
    patients = Patient.query.filter_by(finishFollowup=0).all()
    return Success(data=patients if patients else [])


# 关闭随访提醒（完成随访）(通过用户id以及下次随访时间来查询）
@api.route('/patient/follInfo/<int:pid>/<string:nextFollowupTime>', methods=['PUT'])
@auth.login_required
@edit_need_auth
def update_patient_follInfo(pid, nextFollowupTime):
    patients = Patient.query.filter_by(id=pid, finishFollowup=0,
                                       nextFollowupTime=datetime.strptime(nextFollowupTime, "%Y-%m-%d")).all()
    with db.auto_commit():
        for patient in patients:
            patient.finishFollowup = 1
    return Success()
