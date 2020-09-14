from flask import request

from app.libs.error import Success
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
    json2db(data, Patient)
    return Success()