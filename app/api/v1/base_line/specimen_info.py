from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array
from app.models.base_line import SpecimenInfo, Patient

api = Redprint('specimen_info')

@api.route('/<int:pid>',methods = ['GET'])
def get_specimen_info(pid):
    specimen_info_array = SpecimenInfo.query.filter_by(pid=pid).all()
    return Success(data=specimen_info_array if specimen_info_array else [])


@api.route('/<int:pid>',methods = ['POST'])
@auth.login_required
def add_specimen_info(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
    data["pid"] = pid
    json2db(data, SpecimenInfo)
    return Success()


@api.route('/<int:pid>',methods = ['DELETE'])
@auth.login_required
def del_specimen_info(pid):
    data = request.get_json()
    items = SpecimenInfo.query.filter(SpecimenInfo.is_delete==0,SpecimenInfo.id.in_(data['ids'])).all()
    delete_array(items)
    return Success()

