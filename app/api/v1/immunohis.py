from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.cycle import Immunohis

api = Redprint('immunohis')

# 免疫组化的获取和提交
@api.route('/<int:pid>/<int:treNum>', methods=['GET'])
def get_immunohis(pid, treNum):
    immunohis = Immunohis.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=immunohis if immunohis else {})


@api.route('/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
def add_immunohis(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Immunohis)
    return Success()


@api.route('/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_immunohis(pid, treNum):
    immunohis = Immunohis.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if immunohis.submit():
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_immunohis(pid, treNum):
    immunohis = Immunohis.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if immunohis.finish():
        return Success(msg='监察结束')
    else:
        return SampleStatusError('当前状态无法结束监察')


