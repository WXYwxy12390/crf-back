"""
@author: yours
@file: first_diagnose.py
@time: 2020-09-14 21:26
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.base_line import IniDiaPro, Patient
from app.utils.modification import if_status_allow_modification, record_modification

api = Redprint('first_diagnose')


@api.route('/<int:pid>', methods=['GET'])
def get_first_diagnose(pid):
    first_diagnose = IniDiaPro.query.filter_by(pid=pid).first()
    return Success(data=first_diagnose if first_diagnose else {})


@api.route('/<int:pid>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_first_diagnose(pid):
    data = request.get_json()
    item = IniDiaPro.query.filter_by(pid=pid).first()

    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, 0, 'IniDiaPro'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, 0, 'IniDiaPro', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    data["pid"] = pid
    json2db(data, IniDiaPro)
    return Success()


# @api.route('/doubt/<int:pid>', methods=['POST'])
# @auth.login_required
# def doubt_first_diagnose(pid):
#     data = request.get_json()
#     item = IniDiaPro.query.filter_by(pid=pid).first_or_404()
#     if item.question(data, pid, 0):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/reply/<int:pid>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_first_diagnose(pid, doubt_index):
#     data = request.get_json()
#     item = IniDiaPro.query.filter_by(pid=pid).first_or_404()
#     if item.reply_doubt(data, pid, 0, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()
