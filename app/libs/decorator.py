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


def record_modification(T):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            out = func(*args, **kwargs)
            data = request.get_json()
            if data.get('id'):
                kwargs['id'] = data.get('id')
            pid = kwargs.get('pid')
            treNum = kwargs.get('treNum')

            T_copy = copy.copy(T)
            if T_copy == 'trement':
                tre_rec = TreRec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
                trement = tre_rec.trement
                if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
                    T_copy = OneToFive
                elif trement == 'surgery':
                    T_copy = Surgery
                elif trement == 'radiotherapy':
                    T_copy = Radiotherapy

            processed_data = process_data(T_copy, data)
            obj = get_obj(T_copy, **kwargs)

            if obj is None:
                return out
            elif type(obj) != list:
                # 当状态不是已提交时，不记录修改
                if obj.module_status != ModuleStatus.Submitted.value:
                    return out
                obj.record_modification(processed_data)
                cancel_submit(T_copy, **kwargs)
            else:
                # 当状态不是已提交时，不记录修改。正常情况下，同病人同访视同模块多条记录应该是状态相同。
                for _obj in obj:
                    if _obj.module_status != ModuleStatus.Submitted.value:
                        return out
                for _obj in obj:
                    for _data in processed_data:
                        if _obj.id == _data.get('id'):
                            del _data['id']
                            _obj.record_modification(_data)
                            break
                cancel_submit(T_copy, **kwargs)

            return out

        return wrapper

    return decorator


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


# 将某用户某访视的某模块的所有数据的状态均从已提交修改为未提交
def cancel_submit(T, **kwargs):
    pid = kwargs.get('pid')
    treNum = kwargs.get('treNum')

    if T == Patient:
        obj = T.query.get_or_404(pid)
        obj.cancel_submit()
    elif T in pid_for_one_obj:
        obj = T.query.filter_by(pid=pid).first_or_404()
        obj.cancel_submit()
    elif T in treNum_for_one_obj:
        obj = T.query.filter_by(pid=pid, treNum=treNum).first_or_404()
        obj.cancel_submit()
    elif T in pid_for_many_obj:
        obj_ls = T.query.filter_by(pid=pid).all()
        for obj in obj_ls:
            obj.cancel_submit()
    elif T in treNum_for_many_obj:
        obj_ls = T.query.filter_by(pid=pid, treNum=treNum).all()
        for obj in obj_ls:
            obj.cancel_submit()

    # 有的表和别的表共同属于一个模块。取消提交时要对同模块的其他表也取消提交。
    if T in [OneToFive, Radiotherapy, Surgery]:
        detail_tre_plans = DetailTrePlan.query.filter_by(pid=pid, treNum=treNum).all()
        for detail_tre_plan in detail_tre_plans:
            detail_tre_plan.cancel_submit()
    if T == PastHis:
        drugHistory_ls = DrugHistory.query.filter_by(pid=pid).all()
        for drugHistory in drugHistory_ls:
            drugHistory.cancel_submit()
    if T == DetailTrePlan:
        one_to_five = OneToFive.query.filter_by(pid=pid, treNum=treNum).first()
        surgery = Surgery.query.filter_by(pid=pid, treNum=treNum).first()
        if one_to_five:
            one_to_five.cancel_submit()
        if surgery:
            surgery.cancel_submit()
    if T == DrugHistory:
        pastHis = PastHis.query.filter_by(pid=pid).first()
        if pastHis:
            pastHis.cancel_submit()


# 返回修改的对象，可能是一个也可能是列表
def get_obj(T, **kwargs):
    pid = kwargs.get('pid')
    treNum = kwargs.get('treNum')
    id = kwargs.get('id')
    if T == Patient:
        obj = T.query.get_or_404(pid)
    elif T in pid_for_one_obj:
        obj = T.query.filter_by(pid=pid).first_or_404()
    elif T in treNum_for_one_obj:
        obj = T.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    elif T in [SpecimenInfo, DrugHistory]:
        # 当不传id时，表示是新增一个，而不是在修改。因此不记录。
        if id is None:
            return None
        obj = T.query.filter_by(pid=pid, id=id).first_or_404()
    elif T == DetailTrePlan:
        # 当不传id时，表示是新增一个治疗计划，而不是在修改。因此不记录。
        if id is None:
            return None
        obj = T.query.filter_by(pid=pid, treNum=treNum, id=id).first_or_404()
    elif T == FollInfo:
        obj = T.query.filter_by(pid=pid).all()
    elif T in [ImageExams, Signs, SideEffect]:
        obj = T.query.filter_by(pid=pid, treNum=treNum).all()
    return obj
