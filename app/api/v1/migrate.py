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
from app.models.therapy_record import Surgery, Radiotherapy, OneToFive, TreRec

api = Redprint('migrate')


@api.route('/4_2')
def migrate_4_2():
    items = TreRec.query.filter_by().all()
    with db.auto_commit():
        i = 0
        for item in items:
            if item.is_auto_compute == 1:
                item.compute_FPS_DFS()
                print(i)
                i = i + 1
    return 'ok'

@api.route('/4_17')
def migrate_4_17():
    items = Patient.query.filter_by(researchCenter=23).all()
    with db.auto_commit():
        for item in items:
            item.researchCenter = 1
    return 'ok'

@api.route('/TJ_samples/<int:center_id>')
def migrate_TJ_sample(center_id):
    items = Patient.query.filter(Patient.is_delete==0,Patient.patNumber.like("TJ%")).all()
    p = Patient.query.filter_by(patientName="周苏建").first()
    with db.auto_commit():
        for item in items:
            item.researchCenter = center_id
        if p:
            p.researchCenter = center_id
    return str(len(items))



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
