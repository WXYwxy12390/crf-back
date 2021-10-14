from flask import request
from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.error_code import ParameterException, SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.base_line import Patient
from app.utils.modification import record_modification, if_status_allow_modification

api = Redprint('patient')


@api.route('/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    return Success(data=patient if patient else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_patient(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)

    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(patient, data, pid, 0, 'Patient'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, 0, 'Patient', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    if 'idNumber' in data:
        item = Patient.query.filter(Patient.is_delete == 0, Patient.idNumber == data['idNumber'],
                                    Patient.id != pid, Patient.researchCenter == patient.researchCenter).first()
        if item:
            raise ParameterException(msg='已经存在相同身份证号码。')
    if 'hospitalNumber' in data and patient.hospitalNumber is not None:
        item = Patient.query.filter(Patient.is_delete == 0, Patient.hospitalNumber == data['hospitalNumber'],
                                    Patient.id != pid, Patient.researchCenter == patient.researchCenter).first()
        if item:
            raise ParameterException(msg='已经存在相同住院号。')
    json2db(data, Patient)
    return Success()


# @api.route('/doubt/<int:pid>', methods=['POST'])
# @auth.login_required
# def doubt_patient(pid):
#     data = request.get_json()
#     item = Patient.query.get_or_404(pid)
#     if item.question(data, pid, 0):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/reply/<int:pid>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_patient(pid, doubt_index):
#     data = request.get_json()
#     item = Patient.query.get_or_404(pid)
#     if item.reply_doubt(data, pid, 0, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()
