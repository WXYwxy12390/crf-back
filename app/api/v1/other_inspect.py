"""
@author: yours
@file: other_inspect.py
@time: 2020-09-05 13:59
"""

from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array
from app.models.base_line import Patient
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.therapy_record import TreRec
from app.utils.modification import record_modification, if_status_allow_modification

api = Redprint('other_inspect')


@api.route('/lung_function/<int:pid>/<int:treNum>', methods=['GET'])
def get_lung_function(pid, treNum):
    data = Lung.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=data if data else {})


@api.route('/lung_function/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_lung_function(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    item = Lung.query.filter_by(pid=pid, treNum=treNum).first()

    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, treNum, 'Lung'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, treNum, 'Lung', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    json2db(data, Lung)
    return Success()


# @api.route('/lung_function/doubt/<int:pid>/<int:treNum>', methods=['POST'])
# @auth.login_required
# def doubt_lung_function(pid, treNum):
#     data = request.get_json()
#     item = Lung.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.question(data, pid, treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/lung_function/reply/<int:pid>/<int:treNum>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_lung_function(pid, treNum, doubt_index):
#     data = request.get_json()
#     item = Lung.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.reply_doubt(data, pid, treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


@api.route('/other_exam/<int:pid>/<int:treNum>', methods=['GET'])
def get_other_exam(pid, treNum):
    data = OtherExams.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=data if data else {})


@api.route('/other_exam/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_other_exam(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    item = OtherExams.query.filter_by(pid=pid, treNum=treNum).first()

    # 当存在'modification_des'时，说明需要记录下该修改。
    if 'modification_des' in data.keys():
        if not record_modification(item, data, pid, treNum, 'OtherExams'):
            return SampleStatusError(msg='当前模块状态无法修改数据')
    else:
        if not if_status_allow_modification(pid, treNum, 'OtherExams', False):
            return SampleStatusError(msg='当前模块状态无法修改数据')

    json2db(data, OtherExams)
    return Success()


# @api.route('/other_exam/doubt/<int:pid>/<int:treNum>', methods=['POST'])
# @auth.login_required
# def doubt_other_exam(pid, treNum):
#     data = request.get_json()
#     item = OtherExams.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.question(data, pid, treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/other_exam/reply/<int:pid>/<int:treNum>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_other_exam(pid, treNum, doubt_index):
#     data = request.get_json()
#     item = OtherExams.query.filter_by(pid=pid, treNum=treNum).first_or_404()
#     if item.reply_doubt(data, pid, treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()


@api.route('/image_exam/<int:pid>/<int:treNum>', methods=['GET'])
def get_image_exam(pid, treNum):
    data = ImageExams.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=data if data else [])


@api.route('/image_exam/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_image_exam(pid, treNum):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum

        id = _data.get('id')
        item = ImageExams.query.get_or_404(id) if id is not None else None
        # 当存在'modification_des'时，说明需要记录下该修改。
        if 'modification_des' in _data.keys():
            if not record_modification(item, _data, pid, treNum, 'ImageExams'):
                return SampleStatusError(msg='当前模块状态无法修改数据')
        else:
            if not if_status_allow_modification(pid, treNum, 'ImageExams', False):
                return SampleStatusError(msg='当前模块状态无法修改数据')

        json2db(_data, ImageExams)
    return Success()


@api.route('/image_exam/<int:pid>/<int:treNum>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
@update_time
def del_image_exam(pid, treNum):
    data = request.get_json()
    items = ImageExams.query.filter(ImageExams.is_delete == 0, ImageExams.id.in_(data['ids'])).all()
    delete_array(items)
    return Success()


# @api.route('/image_exam/doubt/<int:image_exam_id>', methods=['POST'])
# @auth.login_required
# def doubt_image_exam(image_exam_id):
#     data = request.get_json()
#     item = ImageExams.query.get_or_404(image_exam_id)
#     if item.question(data, item.pid, item.treNum):
#         return Success()
#     else:
#         return SampleStatusError()
#
#
# @api.route('/image_exam/reply/<int:image_exam_id>/<int:doubt_index>', methods=['POST'])
# @auth.login_required
# def reply_image_exam(image_exam_id, doubt_index):
#     data = request.get_json()
#     item = ImageExams.query.get_or_404(image_exam_id)
#     if item.reply_doubt(data, item.pid, item.treNum, doubt_index):
#         return Success()
#     else:
#         return SampleStatusError()

