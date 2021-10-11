from datetime import timedelta as td, datetime

from flask import request, g,current_app

from app.libs.decorator import edit_need_auth, update_time, record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
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
    if treRec and treRec.is_auto_compute == 1:
        treRec.compute_FPS_DFS()
    return Success(data=treRec if treRec else {})


@api.route('/evaluation/<int:pid>/<int:treNum>/<string:trement>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
# @record_modification(TreRec)
def add_treatment_evaluation(pid, treNum, trement):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    data['trement'] = trement
    json2db(data, TreRec)
    """
    每一次治疗信息中，疗效评估页面，增加一个字段"PFS/DFS"，该字段可以手动录入，也可以系统自动计算填写，自动计算优先于手动填写。
    填写了进展时间之后，系统需要自动计算PFS/DFS，并填写，计算逻辑为：用药开始时间到进展时间之间的时间间隔。如果不自动计算，则可以手动填写
    """
    # if 'proDate' in data and 'PFS_DFS' not in data:
    #     treRec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
    #     treRec.compute_FPS_DFS()
    treRec = TreRec.query.filter_by(pid=pid, treNum=treNum).first()
    if treRec.is_auto_compute == 1:
        treRec.compute_FPS_DFS()
    return Success()


@api.route('/evaluation/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_treatment_evaluation(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module('Evaluation', treNum):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/evaluation/begin_monitor/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def begin_monitor_evaluation(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor('Evaluation', treNum):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/evaluation/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_evaluation(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.finish('Evaluation', treNum):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


@api.route('/evaluation/doubt/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
def doubt_evaluation(pid, treNum):
    data = request.get_json()
    item = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if item.question(data, pid, treNum):
        return Success()
    else:
        return SampleStatusError()


@api.route('/evaluation/reply/<int:pid>/<int:treNum>/<int:doubt_index>', methods=['POST'])
@auth.login_required
def reply_evaluation(pid, treNum, doubt_index):
    data = request.get_json()
    item = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if item.reply_doubt(data, pid, treNum, doubt_index):
        return Success()
    else:
        return SampleStatusError()


# 症状体征的获取、提交、删除
@api.route('/signs/<int:pid>/<int:treNum>', methods=['GET'])
def get_signs(pid, treNum):
    signs = Signs.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=signs if signs else [])


@api.route('/signs/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
# @record_modification(Signs)
def add_signs(pid, treNum):
    data = request.get_json()
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


@api.route('/signs/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_signs(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module('Signs', treNum):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/signs/begin_monitor/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def begin_monitor_signs(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor('Signs', treNum):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/signs/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_signs(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.finish('Signs', treNum):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


@api.route('/signs/doubt/<int:sign_id>', methods=['POST'])
@auth.login_required
def doubt_signs(sign_id):
    data = request.get_json()
    item = Signs.query.get_or_404(sign_id)
    if item.question(data, item.pid, item.treNum):
        return Success()
    else:
        return SampleStatusError()


@api.route('/signs/reply/<int:image_exam_id>/<int:doubt_index>', methods=['POST'])
@auth.login_required
def reply_signs(image_exam_id, doubt_index):
    data = request.get_json()
    item = Signs.query.get_or_404(image_exam_id)
    if item.reply_doubt(data, item.pid, item.treNum, doubt_index):
        return Success()
    else:
        return SampleStatusError()


# 副反应的获取、提交、删除
@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['GET'])
def get_side_effect(pid, treNum):
    side_effect = SideEffect.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=side_effect if side_effect else [])


@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
# @record_modification(SideEffect)
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


@api.route('/side_effect/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_side_effect(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module('SideEffect', treNum):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/side_effect/begin_monitor/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def begin_monitor_side_effect(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor('SideEffect', treNum):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/side_effect/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_side_effect(pid, treNum):
    patient = Patient.query.get_or_404(pid)
    if patient.finish('SideEffect', treNum):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


@api.route('/side_effect/doubt/<int:side_effect_id>', methods=['POST'])
@auth.login_required
def doubt_side_effect(side_effect_id):
    data = request.get_json()
    item = SideEffect.query.get_or_404(side_effect_id)
    if item.question(data, item.pid, item.treNum):
        return Success()
    else:
        return SampleStatusError()


@api.route('/side_effect/reply/<int:image_exam_id>/<int:doubt_index>', methods=['POST'])
@auth.login_required
def reply_side_effect(image_exam_id, doubt_index):
    data = request.get_json()
    item = SideEffect.query.get_or_404(image_exam_id)
    if item.reply_doubt(data, item.pid, item.treNum, doubt_index):
        return Success()
    else:
        return SampleStatusError()


# 随访信息表的获取、提交、删除
@api.route('/follInfo/<int:pid>', methods=['GET'])
def get_follInfo(pid):
    follInfo = FollInfo.query.filter(FollInfo.pid == pid,
                                     FollInfo.is_delete == 0).order_by(FollInfo.date.desc()).all()
    return Success(data=follInfo if follInfo else [])


@api.route('/follInfo/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
# @record_modification(FollInfo)
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


@api.route('/follInfo/submit/<int:pid>', methods=['GET'])
@auth.login_required
def submit_follInfo(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module('FollInfo', 0):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/follInfo/begin_monitor/<int:pid>', methods=['GET'])
@auth.login_required
def begin_monitor_follInfo(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor('FollInfo', 0):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/follInfo/finish/<int:pid>', methods=['GET'])
@auth.login_required
def finish_follInfo(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.finish('FollInfo', 0):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


@api.route('/follInfo/doubt/<int:follInfo_id>', methods=['POST'])
@auth.login_required
def doubt_follInfo(follInfo_id):
    data = request.get_json()
    item = FollInfo.query.get_or_404(follInfo_id)
    if item.question(data, item.pid, 0):
        return Success()
    else:
        return SampleStatusError()


@api.route('/follInfo/reply/<int:specimen_info_id>/<int:doubt_index>', methods=['POST'])
@auth.login_required
def reply_follInfo(specimen_info_id, doubt_index):
    data = request.get_json()
    item = FollInfo.query.get_or_404(specimen_info_id)
    if item.reply_doubt(data, item.pid, 0, doubt_index):
        return Success()
    else:
        return SampleStatusError()


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
