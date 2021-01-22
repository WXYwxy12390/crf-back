import os
import shutil

from flask import jsonify, current_app

from app.libs.redprint import Redprint
from app.models import db, json2db
from app.models.base_line import Patient, PastHis, DrugHistory, IniDiaPro
from app.models.crf_info import FollInfo
from app.models.cycle import Immunohis, MoleDetec
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.therapy_record import Surgery, Radiotherapy, OneToFive

api = Redprint('migrate')


# 迁移update_time
@api.route('/update_time', methods=['GET'])
def migrate_update_time():
    patients = Patient.query.filter_by().all()
    with db.auto_commit():
        for patient in patients:
            patient.update_time = patient.updateTime
    return 'ok'


@api.route('/hormone_drug', methods=['GET'])
def migrate_hormone_drug():
    hormone_items = PastHis.query.filter(PastHis.is_delete == 0, PastHis.hormone == 1).all()
    drug_items = PastHis.query.filter(PastHis.is_delete == 0, PastHis.drug == 1).all()
    with db.auto_commit():
        for item in hormone_items:
            hormones = item.hormoneUseHis
            for hormone in hormones:
                json2db({
                    'pid': item.pid,
                    'type': 1,
                    'drug_name': hormone.get('drugName'),
                    'drug_dose': hormone.get('drugDose'),
                    'use_time': hormone.get('duration') if hormone.get('duration') != '/' else None
                }, DrugHistory)

        for item in drug_items:
            drugs = item.drugUseHis
            for drug in drugs:
                json2db({
                    'pid': item.pid,
                    'type': 0,
                    'drug_name': drug.get('drugName'),
                    'drug_dose': drug.get('drugDose'),
                    'use_time': drug.get('duration') if drug.get('duration') != '/' else None
                }, DrugHistory)
    return 'ok'


# 得先创建一个_gender,然后转换值
@api.route('/gender', methods=['GET'])
def migrate_gender():
    patients = Patient.query.filter_by().all()
    with db.auto_commit():
        for patient in patients:
            if patient._gender == '1':
                patient.gender = 1
            elif patient._gender == '0':
                patient.gender = 0

    return 'ok'


# 迁移既往史
@api.route('/past_history', methods=['GET'])
def migrate_past_history():
    items = PastHis.query.filter_by().all()
    with db.auto_commit():
        for item in items:
            if item._basDisHis:
                strs = item._basDisHis.split(',')
                item.basDisHis = generate_value(strs)
            # if item._infDisHis:
            #     item.infDisHis = generate_value(item._infDisHis)
            # if item._tumHis:
            #     item.tumHis = generate_value(item._tumHis)
            # if item._tumFamHis:
            #     item.tumFamHis = generate_value(item._tumFamHis)

    return 'ok'


# 迁移 初诊过程
@api.route('/IniDiaPro', methods=['GET'])
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

    return 'ok'


# 迁移治疗记录
@api.route('/therapy_record', methods=['GET'])
def migrate_therapy_record():
    with db.auto_commit():
        items = OneToFive.query.filter_by().all()
        radio_array = ['手术', '纵隔镜', '胸腔镜', '肺穿刺', '纤支镜', 'EBUS', 'EUS', '淋巴结活检', '其他']
        for item in items:
            if item._bioMet:
                item.bioMet = generate_value_with_radio_list(item._bioMet, radio_array)

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


@api.route('/patient', methods=['GET'])
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


# 迁移病理诊断
@api.route('/patDia', methods=['GET'])
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


@api.route('/file', methods=['GET'])
def migrate_file():
    # 实验室检查
    migrate_file_from_old(BloodRoutine, 'blood_routine')
    migrate_file_from_old(BloodBio, 'blood_bio')
    migrate_file_from_old(Thyroid, 'thyroid')
    migrate_file_from_old(Coagulation, 'coagulation')
    migrate_file_from_old(MyocardialEnzyme, 'myocardial_enzyme')
    migrate_file_from_old(Cytokines, 'cytokines')
    migrate_file_from_old(LymSubsets, 'lymSubsets')
    migrate_file_from_old(UrineRoutine, 'urineRoutine')
    migrate_file_from_old(TumorMarker, 'tumorMarker')

    # #其他检查
    migrate_file_from_old(Lung, 'lung')
    migrate_file_from_12_lead_ecg(OtherExams, '12_lead_ecg')
    migrate_file_from_ucg(OtherExams, 'UCG')
    migrate_file_from_path(ImageExams, 'image_exams')
    #
    # #免疫组化
    migrate_file_from_old(Immunohis, 'immunohis')
    #
    # #分子检查
    migrate_file_from_path(MoleDetec, 'moleDetec')
    #
    # #随访信息
    migrate_file_from_saveFile(FollInfo, 'follInfo')
    return 'ok'

@api.route('/1_11')
def migrate_1_11():
    ini_items = IniDiaPro.query.filter_by().all()
    ini_dict = {}
    for item in ini_items:
        ini_dict[item.pid] = item
    items = Immunohis.query.filter_by(treNum=0).all()
    with db.auto_commit():
        for item in items:
            if ini_dict.get(item.pid):
                item.Ki67 = ini_dict.get(item.pid).Ki67

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


def generate_value_with_radio_list(str, radio_list):
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


@api.route('/gene')
def migrate_gene():
    olds = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.update_time > "2020-10-22 01:24:00",
                                  MoleDetec.create_time == "2020-10-22 01:23:59").all()
    news = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.create_time > "2020-10-22 01:23:59").all()
    item_list = ['ALK', 'BIM', 'BRAF', 'cMET', 'EGFR', 'HER_2', 'KRAS', 'PIK3CA', 'ROS1', 'RET', 'UGT1A1']
    for old in olds:
        change(old, item_list)
    for new in news:
        change(new, item_list)
    return 'ok'

@api.route('/center')
def migrate_center():
    patient_names = ['王剑','熊隆明',
'李卫',
'李义军',
'陶银清',
'叶生发',
'熊青龙',
'李晓宏',
'易传安',
'付超',
'张远红',
'刘玉荣',
'陈应秀',
'刘支旺',
'陈继',
'陈东初',
'金绍松',
'陈春红',
'密涛',
'刘为军',
'刘继仁',
'邓端友',
'熊元松',
'谢成国',
'方小平',
'刘炳文',
'熊甲吾',
'周俊',
'胡军强',
'郑四清',
'何晓望',
'沈小龙',
'李华平',
'邵国成',
'胡学礼',
'曾小平',
'卢平',
'黄啟疆',
'邹先林',
'李广秀',
'孙章礼',
'冉崇来',
'陈俊',
'金发申',
'苗新珍',
'宋永林',
'周苏建',
'王卫平',
'黄海棠',
'柳学珍',
'丁春梅',
'朱大海',
'杨敬兵',
'陈升其',
'倪超群',
'邱榴华',
'唐敦中',
'刘先模',
'张国民',
'谭明栋',
'陈绪林',
'夏永乐',
'杨光明',
'朱定明',
'廖维兵',
'刘尧清',
'熊旭',
'余国成',
'张迎春',
'陈瑶',
'孙舒文',
'彭义红',
'印永捷',
'刘善军',
'章旺明',
'余小凤',
'王能光',
'汪水英',
'张绪学',
'夏先民',
'龙媛秀',
'郑宏军',
'吴晓',
'陈志',
'曾伶',
'张爱华',
'刘子刚',
'付贵荣',
'杨新建']
    items = Patient.query.filter(Patient.is_delete==0,Patient.patientName.in_(patient_names)).all()
    with db.auto_commit():
        for item in items:
            item.researchCenter = 23
    return 'ok'
def change(model_item,items):
    with db.auto_commit():
        for item in items:
            value = getattr(model_item, item)
            if value is None:
                continue
            if value == 1:
                setattr(model_item, item, 0)
            elif value == 0:
                setattr(model_item, item, 2)
            elif value == 2:
                setattr(model_item, item, 1)


def migrate_file_from_old(model, file_folder):
    items = model.query.filter(model.is_delete == 0, model.filePath != None,
                               model.filePath != '').all()
    for item in items:
        file_list = item.filePath.split(',')
        folder = current_app.static_folder + '/' + file_folder + '/' + str(item.id)
        for file_path in file_list:
            filename = file_path.split('/')[2]
            dstfile = folder + '/' + filename
            srcfile = current_app.static_folder + '/' + file_path
            mycopyfile(srcfile, dstfile)


def migrate_file_from_12_lead_ecg(model, file_folder):
    items = model.query.filter(model.is_delete == 0, model.ECGPath != None,
                               model.ECGPath != '').all()
    for item in items:
        file_list = item.ECGPath.split(',')
        folder = current_app.static_folder + '/' + file_folder + '/' + str(item.id)
        for file_path in file_list:
            filename = file_path.split('/')[2]
            dstfile = folder + '/' + filename
            srcfile = current_app.static_folder + '/' + file_path
            mycopyfile(srcfile, dstfile)


def migrate_file_from_ucg(model, file_folder):
    items = model.query.filter(model.is_delete == 0, model.UCGPath != None,
                               model.UCGPath != '').all()
    for item in items:
        file_list = item.UCGPath.split(',')
        folder = current_app.static_folder + '/' + file_folder + '/' + str(item.id)
        for file_path in file_list:
            filename = file_path.split('/')[2]
            dstfile = folder + '/' + filename
            srcfile = current_app.static_folder + '/' + file_path
            mycopyfile(srcfile, dstfile)


def migrate_file_from_path(model, file_folder):
    items = model.query.filter(model.is_delete == 0, model.path != None,
                               model.path != '').all()
    for item in items:
        file_list = item.path.split(',')
        folder = current_app.static_folder + '/' + file_folder + '/' + str(item.id)
        for file_path in file_list:
            filename = file_path.split('/')[2]
            dstfile = folder + '/' + filename
            srcfile = current_app.static_folder + '/' + file_path
            mycopyfile(srcfile, dstfile)


def migrate_file_from_saveFile(model, file_folder):
    items = model.query.filter(model.is_delete == 0, model.savFilPath != None,
                               model.savFilPath != '').all()
    for item in items:
        file_list = item.savFilPath.split(',')
        folder = current_app.static_folder + '/' + file_folder + '/' + str(item.id)
        for file_path in file_list:
            filename = file_path.split('/')[2]
            dstfile = folder + '/' + filename
            srcfile = current_app.static_folder + '/' + file_path
            mycopyfile(srcfile, dstfile)


def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
