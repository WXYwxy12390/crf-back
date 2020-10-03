from flask import request

from app.libs.error import Success
from app.libs.error_code import ParameterException
from app.libs.redprint import Redprint
from app.models import json2db
from app.models.base_line import Patient

api = Redprint('patient')

@api.route('/<int:id>',methods = ['GET'])
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    return Success(data=patient if patient else {})


@api.route('/<int:id>',methods = ['POST'])
def add_patient(id):
    data = request.get_json()
    if 'idNumber' in data:
        patient = Patient.query.filter(Patient.is_delete==0,Patient.idNumber==data['idNumber'],Patient.id!=id).first()
        if patient:
            raise ParameterException(msg='已经存在相同身份证号码。')
    json2db(data, Patient)
    return Success()