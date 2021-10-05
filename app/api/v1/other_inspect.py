"""
@author: yours
@file: other_inspect.py
@time: 2020-09-05 13:59
"""

from flask import request

from app.libs.decorator import edit_need_auth, update_time, record_modification
from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db, db, delete_array
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.therapy_record import TreRec

api = Redprint('other_inspect')


@api.route('/lung_function/<int:pid>/<int:treNum>', methods=['GET'])
def get_lung_function(pid, treNum):
    data = Lung.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=data if data else {})


@api.route('/lung_function/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(Lung)
def add_lung_function(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Lung)
    return Success()


@api.route('/lung_function/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_lung(pid, treNum):
    lung = Lung.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if lung.submit():
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/lung_function/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_lung(pid, treNum):
    lung = Lung.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if lung.finish():
        return Success(msg='监察结束')
    else:
        return SampleStatusError('当前状态无法结束监察')


@api.route('/other_exam/<int:pid>/<int:treNum>', methods=['GET'])
def get_other_exam(pid, treNum):
    data = OtherExams.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=data if data else {})


@api.route('/other_exam/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(OtherExams)
def add_other_exam(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, OtherExams)
    return Success()


@api.route('/other_exam/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_other_exam(pid, treNum):
    other_exam = OtherExams.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if other_exam.submit():
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/other_exam/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_other_exam(pid, treNum):
    other_exam = OtherExams.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if other_exam.finish():
        return Success(msg='监察结束')
    else:
        return SampleStatusError('当前状态无法结束监察')


@api.route('/image_exam/<int:pid>/<int:treNum>', methods=['GET'])
def get_image_exam(pid, treNum):
    data = ImageExams.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=data if data else [])


@api.route('/image_exam/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(ImageExams)
def add_image_exam(pid, treNum):
    data = request.get_json()
    imageExam = ImageExams.query.filter_by(pid=pid, treNum=treNum).first()

    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        _data['module_status'] = imageExam.module_status if imageExam else 0
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


@api.route('/image_exam/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_image_exam(pid, treNum):
    exams = ImageExams.query.filter_by(pid=pid, treNum=treNum).all()
    for exam in exams:
        if exam.module_status != ModuleStatus.UnSubmitted.value:
            return SampleStatusError('当前状态无法提交')
    for exam in exams:
        exam.submit()
    return Success(msg='提交成功')


@api.route('/image_exam/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_image_exam(pid, treNum):
    exams = ImageExams.query.filter_by(pid=pid, treNum=treNum).all()
    for exam in exams:
        if exam.module_status != ModuleStatus.Submitted.value:
            return SampleStatusError('当前状态无法结束监察')
    for exam in exams:
        exam.finish()
    return Success(msg='监察结束')