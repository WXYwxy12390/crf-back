from flask import jsonify

from app.libs.redprint import Redprint
from app.models import db, json2db
from app.models.base_line import Patient, PastHis, DrugHistory

api = Redprint('migrate')
#迁移update_time
@api.route('/update_time',methods=['GET'])
def migrate_update_time():
    patients = Patient.query.filter_by().all()
    with db.auto_commit():
        for patient in patients:
            patient.update_time = patient.updateTime
    return 'ok'

@api.route('/hormone_drug',methods=['GET'])
def migrate_hormone_drug():
    hormone_items = PastHis.query.filter(PastHis.is_delete==0,PastHis.hormone==1).all()
    drug_items = PastHis.query.filter(PastHis.is_delete == 0, PastHis.drug == 1).all()
    with db.auto_commit():
        for item in hormone_items:
            hormones = item.hormoneUseHis
            for hormone in hormones:

                json2db({
                    'pid':item.pid,
                    'type':1,
                    'drug_name':hormone.get('drugName'),
                    'drug_dose':hormone.get('drugDose'),
                    'use_time':hormone.get('duration')
                },DrugHistory)

        for item in drug_items:
            drugs = item.drugUseHis
            for drug in drugs:

                json2db({
                    'pid':item.pid,
                    'type':0,
                    'drug_name':drug.get('drugName'),
                    'drug_dose':drug.get('drugDose'),
                    'use_time':drug.get('duration')
                },DrugHistory)
    return 'ok'

@api.route('/gender',methods=['GET'])
def migrate_gender():
    patients = Patient.query.filter_by().all()
    with db.auto_commit():
        for patient in patients:
            if patient.gender == '1':
                patient._gender = 1
            elif patient.gender == '0':
                patient._gender = 0

    return 'ok'

