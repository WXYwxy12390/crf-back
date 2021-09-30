import copy
from datetime import datetime
from functools import wraps

from flask import request, g

from app.libs.enums import ModuleStatus
from app.libs.error_code import ParameterException
from app.models import db
from app.models.base_line import Patient, PastHis, IniDiaPro, SpecimenInfo
from app.models.cycle import Immunohis, MoleDetec
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.spider.user_info import UserInfo

pid_for_one_obj = [PastHis, IniDiaPro]
pid_for_many_obj = [SpecimenInfo]
treNum_for_one_obj = [BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, LymSubsets,
                      UrineRoutine, TumorMarker, Lung, OtherExams, Immunohis, MoleDetec]
treNum_for_many_obj = [ImageExams]


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

            data = copy.copy(request.get_json())
            data_keys = data.keys()

            if 'id' in data_keys:
                kwargs['id'] = data['id']
                del data['id']
            if 'pid' in data_keys:
                del data['pid']
            if 'treNum' in data_keys:
                del data['treNum']

            obj = get_obj(T, **kwargs)
            if obj is None:
                return out
            elif type(obj) != list:
                # 当状态不是已提交时，不记录修改
                if obj.module_status != ModuleStatus.Submitted.value:
                    return out
                obj.record_modification(data)
                cancel_submit(T, **kwargs)
            else:
                data_ls = data.get('data')
                # 当状态不是已提交时，不记录修改。正常情况下，同病人同访视同模块多条记录应该是状态相同。
                for _obj in obj:
                    if _obj.module_status != ModuleStatus.Submitted.value:
                        return out

                for _obj in obj:
                    for data in data_ls:
                        if _obj.id == data.get('id'):
                            del data['id']
                            _obj.record_modification(data)
                            break
                cancel_submit(T, **kwargs)

            return out

        return wrapper

    return decorator


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
    elif T == SpecimenInfo:
        # 当不传id时，表示是新增一个标本信息，而不是在修改。因此不记录。
        if id is None:
            return None
        obj = T.query.filter_by(pid=pid, id=id).first_or_404()
    elif T in treNum_for_many_obj:
        obj = T.query.filter_by(pid=pid, treNum=treNum).all()
    return obj
