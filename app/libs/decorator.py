from datetime import datetime
from functools import wraps

from flask import request, g

from app.libs.enums import SampleStatus, interface_dict
from app.libs.error_code import SubmitError, ParameterException
from app.models import db
from app.models.base_line import Patient
from app.spider.user_info import UserInfo


def sample_no_submit(func):
    @wraps(func)
    def wrapper(**kwargs):
        # 样本已提交,则不能修改
        sample = Sample.query.get_or_404(kwargs['sample_id'])
        if sample.submit_status == SampleStatus.AllSubmit.value:
            return SubmitError()

        return func(**kwargs)

    return wrapper


def cycle_no_submit(func):
    @wraps(func)
    def wrapper(**kwargs):
        cycle_number = kwargs['cycle_number'] if kwargs.get('cycle_number') else 1
        # 治疗期随访已提交,则不能修改
        cycle = Cycle.query.filter_by(sample_id=kwargs["sample_id"],
                                      cycle_number=cycle_number).first_or_404()
        if cycle.is_submit == 1:
            return SubmitError(msg="当前访视已提交,无法进行修改")

        return func(**kwargs)

    return wrapper


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
        if pid is None :
            raise ParameterException(msg='未传pid')
        else:
            patient = Patient.query.get_or_404(pid)
            with db.auto_commit():
                patient.update_time = datetime.now()
        return out
    return call

def generate_modify_content(endpoint,cycle_number):
    pre_fix = '访视'
    if cycle_number:
        pre_fix = pre_fix + str(cycle_number)
    elif endpoint == 'v1.summary+add_summary':
        pre_fix = '项目总结'
    else:
        pre_fix = '访视1'
    return pre_fix + '-' + interface_dict.get(endpoint)









