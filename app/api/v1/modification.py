import copy

from flask import request
from sqlalchemy.orm.attributes import flag_modified
from app.libs.error import Success, APIException
from app.libs.error_code import SubmitError, SampleStatusError, ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import db
from app.models.base_line import Patient, IniDiaPro, PastHis, SpecimenInfo, DrugHistory
from app.models.crf_info import FollInfo
from app.models.cycle import Immunohis, MoleDetec, Signs, SideEffect
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker

from app.models.other_inspect import ImageExams, Lung, OtherExams
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy, DetailTrePlan

api = Redprint('modification')

modules = ['Patient', 'IniDiaPro', 'PastHis', 'SpecimenInfo', 'FollInfo',
           'BloodRoutine', 'BloodBio', 'Thyroid', 'Coagulation', 'MyocardialEnzyme',
           'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker',
           'Lung', 'OtherExams', 'ImageExams',
           'Immunohis', 'MoleDetec',
           'TreRec', 'Evaluation', 'Signs', 'SideEffect']

name_to_class = {
    'Patient': Patient, 'IniDiaPro': IniDiaPro, 'PastHis': PastHis, 'DrugHistory': DrugHistory,
    'SpecimenInfo': SpecimenInfo, 'FollInfo': FollInfo,
    'BloodRoutine': BloodRoutine, 'BloodBio': BloodBio, 'Thyroid': Thyroid, 'Coagulation': Coagulation,
    'MyocardialEnzyme': MyocardialEnzyme, 'Cytokines': Cytokines, 'LymSubsets': LymSubsets,
    'UrineRoutine': UrineRoutine, 'TumorMarker': TumorMarker,
    'Lung': Lung, 'OtherExams': OtherExams, 'ImageExams': ImageExams,
    'Immunohis': Immunohis, 'MoleDetec': MoleDetec,
    'Evaluation': TreRec,
    'OneToFive': OneToFive, 'Surgery': Surgery, 'Radiotherapy': Radiotherapy,
    'DetailTrePlan': DetailTrePlan, 'Signs': Signs, 'SideEffect': SideEffect
}


@api.route('/submit_cycle/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_cycle(pid, treNum):
    all_baseLine_modules = ['Patient', 'IniDiaPro', 'PastHis', 'SpecimenInfo', 'BloodRoutine', 'BloodBio', 'Thyroid',
                            'Coagulation', 'MyocardialEnzyme', 'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker',
                            'Lung', 'OtherExams', 'ImageExams', 'Immunohis', 'MoleDetec', 'FollInfo']
    all_treRec_modules = ['TreRec', 'BloodRoutine', 'BloodBio', 'Thyroid', 'Coagulation', 'MyocardialEnzyme',
                          'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker', 'Lung', 'OtherExams', 'ImageExams',
                          'Immunohis', 'MoleDetec', 'Evaluation', 'Signs', 'SideEffect']
    flag = False  # 标志是否可以提交访视。若已提交，则无法重复提交。
    # 当提交访视时，会把该访视的所有模块全部提交
    treNum_str = str(treNum)
    patient = Patient.query.get_or_404(pid)
    if treNum == 0:
        for module in all_baseLine_modules:
            patient.submit_module(module, treNum)
    else:
        for module in all_treRec_modules:
            patient.submit_module(module, treNum)

    cycle_is_submit = copy.copy(patient.cycle_is_submit)
    if cycle_is_submit is None:
        cycle_is_submit = {}
    if cycle_is_submit.get(treNum_str) is None or cycle_is_submit.get(treNum_str) == 0:
        cycle_is_submit[treNum_str] = 1
        flag = True
    with db.auto_commit():
        patient.cycle_is_submit = cycle_is_submit
        flag_modified(patient, 'cycle_is_submit')
    if flag:
        return Success(msg='提交成功')
    else:
        return SubmitError(msg='该访视已提交')


@api.route('/submit/<string:module>/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit(module, pid, treNum):
    if module not in modules:
        return ParameterException(msg='模块名错误')
    patient = Patient.query.get_or_404(pid)
    if patient.submit_module(module, treNum):
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/begin_monitor/<string:module>/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def begin_monitor(module, pid, treNum):
    if module not in modules:
        return ParameterException(msg='模块名错误')
    patient = Patient.query.get_or_404(pid)
    if patient.start_monitor(module, treNum):
        return Success(msg='启动监察成功')
    else:
        return SampleStatusError(msg='启动监察失败')


@api.route('/finish/<string:module>/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish(module, pid, treNum):
    if module not in modules:
        return ParameterException(msg='模块名错误')
    patient = Patient.query.get_or_404(pid)
    if patient.finish(module, treNum):
        return Success(msg='监察已完成')
    else:
        return SampleStatusError('当前无法完成监察')


# item_id是对应表里的主键id。
# 在某些表中，每个样本的每个访视有多条数据，比如影像学检查、副反应、随访信息等等。质疑这些表时一定要传item_id。
# 但质疑其余表时，可以令item_id为0，表示不使用item_id.
@api.route('/doubt/<string:class_name>/<int:pid>/<int:treNum>/<int:item_id>', methods=['POST'])
@auth.login_required
def doubt(class_name, pid, treNum, item_id):
    if class_name not in name_to_class.keys():
        return ParameterException(msg='class_name错误')
    # 在质疑下列几个表的数据时，由于这些表每个样本有多条数据，所以除了传pid和treNum,一定要传相应表id
    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan'] \
            and item_id == 0:
        return ParameterException(msg='id错误')

    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan']:
        item = name_to_class[class_name].query.get_or_404(item_id)
    elif class_name == 'Patient':
        item = name_to_class[class_name].query.get_or_404(pid)
    elif class_name in ['IniDiaPro', 'PastHis']:
        item = name_to_class[class_name].query.filter_by(pid=pid).first_or_404()
    else:
        item = name_to_class[class_name].query.filter_by(pid=pid, treNum=treNum).first_or_404()

    data = request.get_json()
    if item.question(data, pid, treNum):
        return Success()
    else:
        return SampleStatusError()


# item_id是对应表里的主键id。
# 在某些表中，每个样本的每个访视有多条数据，比如影像学检查、副反应、随访信息等等。回复这些表时一定要传item_id。
# 但回复其余表时，可以令item_id为0，表示不使用item_id.
@api.route('/reply/<int:doubt_index>/<string:class_name>/<int:pid>/<int:treNum>/<int:item_id>', methods=['POST'])
@auth.login_required
def reply(doubt_index, class_name, pid, treNum, item_id):
    if class_name not in name_to_class.keys():
        return ParameterException(msg='class_name错误')
    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan'] \
            and item_id == 0:
        return ParameterException(msg='id错误')

    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan']:
        item = name_to_class[class_name].query.get_or_404(item_id)
    elif class_name == 'Patient':
        item = name_to_class[class_name].query.get_or_404(pid)
    elif class_name in ['IniDiaPro', 'PastHis']:
        item = name_to_class[class_name].query.filter_by(pid=pid).first_or_404()
    else:
        item = name_to_class[class_name].query.filter_by(pid=pid, treNum=treNum).first_or_404()

    data = request.get_json()
    if item.reply_doubt(data, item.pid, item.treNum, doubt_index):
        return Success()
    else:
        return SampleStatusError()


@api.route('/history/<string:class_name>/<int:pid>/<int:treNum>/<int:item_id>', methods=['GET'])
@auth.login_required
def get_history(class_name, pid, treNum, item_id):
    if class_name not in name_to_class.keys():
        return ParameterException(msg='class_name错误')
    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan'] \
            and item_id == 0:
        return ParameterException(msg='id错误')

    if class_name in ['DrugHistory', 'SpecimenInfo', 'FollInfo', 'ImageExams', 'Signs', 'SideEffect', 'DetailTrePlan']:
        item = name_to_class[class_name].query.get_or_404(item_id)
    elif class_name == 'Patient':
        item = name_to_class[class_name].query.get_or_404(pid)
    elif class_name in ['IniDiaPro', 'PastHis']:
        item = name_to_class[class_name].query.filter_by(pid=pid).first_or_404()
    else:
        item = name_to_class[class_name].query.filter_by(pid=pid, treNum=treNum).first_or_404()

    data = item.get_history()
    return Success(data=data if data else {})


