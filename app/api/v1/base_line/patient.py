from flask import request, g

from app.libs.decorator import edit_need_auth, record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import ParameterException, SubmitError, SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db
from app.models.base_line import Patient
from app.spider.user_info import UserInfo

api = Redprint('patient')


@api.route('/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    return Success(data=patient if patient else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@record_modification(Patient)
def add_patient(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
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


@api.route('/submit/<int:pid>', methods=['GET'])
@auth.login_required
def submit_patient(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.submit():
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/finish/<int:pid>', methods=['GET'])
@auth.login_required
def finish_patient(pid):
    patient = Patient.query.get_or_404(pid)
    if patient.finish():
        return Success(msg='监察结束')
    else:
        return SampleStatusError('当前状态无法结束监察')
