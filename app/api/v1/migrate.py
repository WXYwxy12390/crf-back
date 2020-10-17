from flask import jsonify

from app.libs.redprint import Redprint
from app.models import db, json2db
from app.models.base_line import Patient, PastHis, DrugHistory, IniDiaPro
from app.models.therapy_record import Surgery, Radiotherapy, OneToFive

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

#得先创建一个_gender,然后转换值
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

#迁移既往史
@api.route('/past_history',methods=['GET'])
def migrate_past_history():
    items = PastHis.query.filter_by().all()
    with db.auto_commit():
        for item in items:
            # if item.basDisHis:
            #     strs = item.basDisHis.split(',')
            #     item._basDisHis = generate_value(strs)
            if item.infDisHis:
                item._infDisHis = generate_value(item.infDisHis)
            if item.tumHis:
                item._tumHis = generate_value(item.tumHis)
            if item.tumFamHis:
                item._tumFamHis = generate_value(item.tumFamHis)

    return 'ok'

#迁移 初诊过程
@api.route('/IniDiaPro',methods=['GET'])
def migrate_ini_dia_pro():
    items = IniDiaPro.query.filter_by().all()
    with db.auto_commit():
        for item in items:
            if item._cliniManifest:
                item.cliniManifest = generate_value(item._cliniManifest)
            if item._part:
                item.part = generate_value(item._part)
            if item._bioMet:
                item.bioMet = generate_value(item._bioMet)
            if item._traSite:
                item.traSite = generate_value(item._traSite)

    return  'ok'

#迁移治疗记录
@api.route('/therapy_record',methods=['GET'])
def migrate_therapy_record():
    with db.auto_commit():
        items = OneToFive.query.filter_by().all()
        radio_array = ['手术','纵隔镜','胸腔镜','肺穿刺','纤支镜','EBUS','EUS','淋巴结活检','其他']
        for item in items:
            if item._bioMet:
                item.bioMet = generate_value_with_radio_list(item._bioMet,radio_array)

    with db.auto_commit():
        items = Surgery.query.filter_by().all()
        for item in items:
            if item._surSco:
                item.surSco = generate_value(item._surSco)
            if item._lymDis:
                item.lymDis = generate_value(item._lymDis)

    with db.auto_commit():
        items = Radiotherapy.query.filter_by().all()
        for item in items:
            if item._radSite:
                item.radSite = generate_value(item._radSite)
    return 'ok'

@api.route('/patient',methods=['GET'])
def migrate_patient():
    patients = Patient.query.filter_by().all()
    with db.auto_commit():
        for patient in patients:
            if patient._researchCenter:
                strs = patient._researchCenter[1:-1].split(',')
                ids = list(set([int(str) for str in strs if str != '']))
                if ids and ids != []:
                    patient.researchCenter = ids[0]
            if patient._account:
                strs = patient._account.strip(',').split(',')
                if strs:
                    ids = list(set([int(str) for str in strs if str != '']))
                    if ids and ids != []:
                        patient.account = ids



    return 'ok'


#迁移病理诊断
@api.route('/patDia',methods = ['GET'])
def migrate_patDia():
    items = IniDiaPro.query.filter_by().all()
    with db.auto_commit():
        for item in items:
            if item._patDia:
                item.patDia = generate_value(item._patDia)
                if item._patDiaOthers:
                    item.patDia['other'] = item._patDiaOthers

    with db.auto_commit():
        items = OneToFive.query.filter_by().all()
        for item in items:
            if item.patDiaRes:
                item.patDia = generate_value(item.patDiaRes)
                if item.patDiaOthers:
                    item.patDia['other'] = item.patDiaOthers
    return 'ok'

def generate_value(str):
    if type(str) is list:
        strs = str
    else:
        strs = str.split(',')
    data = {
        'radio': [],
        'other': None
    }
    i = 0
    while i < len(strs):
        if strs[i] != '' and strs[i] != '其他':
            data['radio'].append(strs[i])
            i = i + 1
        elif strs[i] == '其他':
            data['other'] = ''
            if i + 1 < len(strs):
                data['other'] = strs[i + 1]
                i = i + 2
            else:
                i = i + 1
        else:
            i = i + 1
    return data

def generate_value_with_radio_list(str,radio_list):
    if type(str) is list:
        strs = str
    else:
        strs = str.split(',')
    data = {
        'radio': [],
        'other': None
    }
    i = 0
    while i < len(strs):
        if strs[i] != '' and strs[i] != '其他' and strs[i] in radio_list:
            data['radio'].append(strs[i])
            i = i + 1
        elif strs[i] == '其他':
            data['other'] = ''
            i = i + 1
        else:
            if data['other'] is None:
                data['other'] = ''
            data['other'] += strs[i]
            i = i + 1
    return data