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
    research = json2db_add(data, Research)
    json2db_add({'uid': g.user.user_id, 'rid': research.id}, ResearchUser)
    return Success()


@api.route('/<int:rid>', methods=['DELETE'])
@auth.login_required
def del_research_by_rid(rid):
    item = Research.query.get_or_404(rid)
    item.delete()
    return Success()


@api.route('/all', methods=['GET'])
@auth.login_required
def get_all_research():
    uid = g.user.user_id
    # 返回当前用户有权限的所有研究
    research_user_list = ResearchUser.query.filter_by(uid=uid).all()
    rids = [research_user.rid for research_user in research_user_list]
    items = Research.query.filter(Research.is_delete == 0,
                                  Research.id.in_(rids)).all()
    return Success(data=items if items else [])


@api.route('/get_patients/<int:rid>', methods=['GET'])
@auth.login_required
def get_patients_by_research(rid):
    args = request.args.to_dict()
    page = int(args.get('page')) if args.get('page') else 1
    limit = int(args.get('limit')) if args.get('limit') else 20
    sort = int(args.get('sort')) if args.get('sort') else None
    flag = ResearchUser.if_user_in_research(g.user.user_id, rid)
    user = g.user
    if flag:
        pids = ResearchPatient.get_patients_by_research(rid, user)
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
