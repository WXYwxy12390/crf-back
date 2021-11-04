from app.libs.error import Success, APIException
from app.libs.error_code import NotFound, ParameterException, Forbidden
from app.libs.redprint import Redprint
from flask import request, g

from app.libs.token_auth import auth
from app.models import json2db_add, db
from app.models.base_line import Patient
from app.models.research import Research
from app.models.researchPatient import ResearchPatient
from app.models.researchUser import ResearchUser
from app.utils.paging import get_paging
from app.utils.sort import sort_samples_while_query

api = Redprint('research')


@api.route('', methods=['POST'])
@auth.login_required
def create_research():
    data = request.get_json()
    research_name = data.get('name')
    if not research_name:
        return ParameterException()
    if Research.get_by_name(research_name):
        return APIException(msg='该名称的研究已存在，请输入其他名称')
    item = json2db_add(data, Research)
    return Success(data=item)


@api.route('/<int:rid>', methods=['DELETE'])
@auth.login_required
def del_research_by_rid(rid):
    item = Research.query.get_or_404(rid)
    item.delete()
    return Success()


@api.route('/<int:rid>', methods=['GET'])
@auth.login_required
def get_research_by_rid(rid):
    item = Research.query.get_or_404(rid)
    return Success(data=item)


@api.route('/all', methods=['GET'])
@auth.login_required
def get_all_research():
    items = Research.query.filter_by().all()
    return Success(data=items)


@api.route('/get_patients/<int:rid>', methods=['GET'])
@auth.login_required
def get_patients_by_research(rid):
    args = request.args.to_dict()
    page = int(args.get('page')) if args.get('page') else 1
    limit = int(args.get('limit')) if args.get('limit') else 20
    sort = int(args.get('sort')) if args.get('sort') else None
    flag = ResearchUser.if_user_in_research(g.user.user_id, rid)
    if flag:
        pids = ResearchPatient.get_patients_by_research(rid)
        patients = sort_samples_while_query(Patient.query.filter(Patient.id.in_(pids)), sort)
        res, total = get_paging(patients, page, limit)
        res = [patient.get_fotmat_info() for patient in res]
        data = {
            "code": 200,
            "msg": "获取样本成功",
            "data": res,
            "total": total,
            "all_pids": pids
        }
        return Success(data=data)
    else:
        return Forbidden(msg='当前用户无法查看该研究')


@api.route('/add_patients', methods=['POST'])
@auth.login_required
def add_patients_to_research():
    data = request.get_json()
    rid = data['rid']
    pids = data['pids']
    ResearchPatient.add_patients_to_research(rid, pids)
    return Success()


@api.route('/remove_patients', methods=['DELETE'])
@auth.login_required
def remove_patients_from_research():
    data = request.get_json()
    rid = data['rid']
    pids = data['pids']
    ResearchPatient.remove_patients_from_research(rid, pids)
    return Success()
