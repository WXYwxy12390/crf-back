import copy
from datetime import datetime
from functools import wraps

from flask import request, g

from app.libs.enums import ModuleStatus
from app.libs.error_code import ParameterException
from app.models import db
from app.models.base_line import Patient, PastHis, IniDiaPro, SpecimenInfo, DrugHistory
from app.models.crf_info import FollInfo
from app.models.cycle import Immunohis, MoleDetec, Signs, SideEffect
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.therapy_record import TreRec, OneToFive, Radiotherapy, Surgery, DetailTrePlan
from app.spider.user_info import UserInfo

pid_for_one_obj = [PastHis, IniDiaPro]
pid_for_many_obj = [SpecimenInfo, FollInfo, DrugHistory]
treNum_for_one_obj = [BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, LymSubsets,
                      UrineRoutine, TumorMarker, Lung, OtherExams, Immunohis, MoleDetec,
                      TreRec, OneToFive, Surgery, Radiotherapy]
treNum_for_many_obj = [ImageExams, Signs, SideEffect, DetailTrePlan]


def post_not_null(func):
    @wraps(func)
    def wrapper(**kwargs):
        if request.method == 'POST' and request.get_json() == {}:  # post 不能为空
            raise ParameterException(msg='不可提交空数据')
        return func(**kwargs)

    return wrapper


def edit_need_auth(func):
    @wraps(func)
    def wrapper(**kwargs):
        if 'OperateAllCRF' in g.user.scopes:
            return func(**kwargs)
        elif 'EditCenterCRF' in g.user.scopes:
            return func(**kwargs)
        patient = Patient.query.get_or_404(kwargs.get('pid'))
        user = UserInfo().search_by_uid(g.user.user_id)['data']
        if patient.researchCenter == user['research_center_id']:
            return func(**kwargs)
        return func(**kwargs)

    return wrapper


def update_time(func):
    @wraps(func)
    def call(*args, **kwargs):
        out = func(*args, **kwargs)
        pid = kwargs.get('pid')
        if pid is None:
            raise ParameterException(msg='未传pid')
        else:
            patient = Patient.query.get_or_404(pid)
            with db.auto_commit():
                patient.update_time = datetime.now()
        return out

    return call


def process_data(T, data):
    data = copy.copy(data)

    if T in [OneToFive, Surgery, Radiotherapy]:
        data = data.get('child')
    elif T in [ImageExams, Signs, SideEffect, FollInfo]:
        data = data.get('data')

    if type(data) == list:
        for _data in data:
            if _data.get('pid'):
                del _data['pid']
            if _data.get('treNum'):
                del _data['treNum']
        return data

    # 修改记录中不用保存id，pid，trNum的变化
    if data.get('id'):
        del data['id']
    if data.get('pid'):
        del data['pid']
    if data.get('treNum'):
        del data['treNum']
    return data

