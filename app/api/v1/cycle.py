import copy
from sqlalchemy.orm.attributes import flag_modified
from app.libs.error import Success
from app.libs.error_code import SubmitError
from app.libs.redprint import Redprint
from app.models import db
from app.models.base_line import Patient

api = Redprint('cycle')


@api.route('/submit/<int:pid>/<int:treNum>', methods=['GET'])
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
