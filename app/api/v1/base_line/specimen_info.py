from flask import request, jsonify

from app.libs.decorator import record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array
from app.models.base_line import SpecimenInfo, Patient
from app.utils.export import Export

api = Redprint('specimen_info')


# 返回一个样本列表，只有标本信息和姓名、住院号、身份证号、编号这几个基本信息
@api.route('/all', methods=['POST', 'GET'])
@auth.login_required
def get_specimen_info_all():
    all_patients = Patient.query.filter_by().order_by(Patient.update_time.desc()).all()
    all_specimen_info = SpecimenInfo.query.filter_by().order_by(SpecimenInfo.update_time.desc()).all()
    all_pids = [patient.id for patient in all_patients]
    buffer = {'patient': Export.classify_by_pid(all_patients),
              'specimen_info': Export.array_classify_by_pid(all_specimen_info)}
    res = []
    for pid in all_pids:
        dic = {}
        patient = buffer['patient'].get(pid)
        specimen_info = buffer['specimen_info'].get(pid)
        dic['pid'] = pid
        dic['patientName'] = patient.patientName
        dic['hospitalNumber'] = patient.hospitalNumber
        dic['idNumber'] = patient.idNumber
        dic['patNumber'] = patient.patNumber
        dic['specimen_info'] = specimen_info
        res.append(dic)
    data = {
        "code": 200,
        "msg": "获取样本成功",
        "data": res,
        "all_pids": all_pids
    }
    return Success(data=res)


@api.route('/<int:pid>', methods=['GET'])
@auth.login_required
def get_specimen_info(pid):
    specimen_info_array = SpecimenInfo.query.filter_by(pid=pid).all()
    return Success(data=specimen_info_array if specimen_info_array else [])


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@record_modification(SpecimenInfo)
def add_specimen_info(pid):
    data = request.get_json()
    data["pid"] = pid

    # 状态和同病人同的其他标本信息一致
    specimenInfo = SpecimenInfo.query.filter_by(pid=pid).first_or_404()
    data['module_status'] = specimenInfo.module_status

    json2db(data, SpecimenInfo)
    return Success()


@api.route('/<int:pid>', methods=['DELETE'])
@auth.login_required
def del_specimen_info(pid):
    data = request.get_json()
    items = SpecimenInfo.query.filter(SpecimenInfo.is_delete == 0, SpecimenInfo.id.in_(data['ids'])).all()
    delete_array(items)
    return Success()


@api.route('/submit/<int:pid>', methods=['GET'])
@auth.login_required
def submit_image_exam(pid):
    specimen_ls = SpecimenInfo.query.filter_by(pid=pid).all()
    for specimen in specimen_ls:
        if specimen.module_status != ModuleStatus.UnSubmitted.value:
            return SampleStatusError('当前状态无法提交')
    for specimen in specimen_ls:
        specimen.submit()
    return Success(msg='提交成功')


@api.route('/finish/<int:pid>', methods=['GET'])
@auth.login_required
def finish_image_exam(pid):
    specimen_ls = SpecimenInfo.query.filter_by(pid=pid).all()
    for specimen in specimen_ls:
        if specimen.module_status != ModuleStatus.Submitted.value:
            return SampleStatusError('当前状态无法结束监察')
    for specimen in specimen_ls:
        specimen.finish()
    return Success(msg='监察结束')
