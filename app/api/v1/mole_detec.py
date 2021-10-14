from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.base_line import Patient
from app.models.cycle import MoleDetec
from app.utils.modification import record_modification, if_status_allow_modification

api = Redprint('mole_detec')

# 分子检测的获取和提交
@api.route('/<int:pid>/<int:treNum>', methods=['GET'])
def get_mole_detec(pid, treNum):
    mole_detec = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=mole_detec if mole_detec else {})


@api.route('/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_mole_detec(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    item = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first()

    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, treNum, 'MoleDetec'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, treNum, 'MoleDetec', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    json2db(data, MoleDetec)
    return Success()


# @api.route('/doubt/<int:pid>/<int:treNum>', methods=['POST'])
# @auth.login_required
# def doubt_moleDetec(pid, treNum):
#     data = request.get_json()
#     item = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.question(data, pid, treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/reply/<int:pid>/<int:treNum>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_moleDetec(pid, treNum, doubt_index):
#     data = request.get_json()
#     item = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.reply_doubt(data, pid, treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


