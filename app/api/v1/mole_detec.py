from flask import request

from app.libs.decorator import edit_need_auth, update_time
from app.libs.error import Success
from app.libs.error_code import SampleStatusError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.cycle import MoleDetec

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
    json2db(data, MoleDetec)
    return Success()


@api.route('/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_moleDetec(pid, treNum):
    moleDetec = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if moleDetec.submit():
        return Success(msg='提交成功')
    else:
        return SampleStatusError('当前状态无法提交')


@api.route('/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_moleDetec(pid, treNum):
    moleDetec = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if moleDetec.finish():
        return Success(msg='监察结束')
    else:
        return SampleStatusError('当前状态无法结束监察')


@api.route('/doubt/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
def doubt_moleDetec(pid, treNum):
    data = request.get_json()
    item = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if item.question(data):
        return Success()
    else:
        return SampleStatusError()


@api.route('/reply/<int:pid>/<int:treNum>/<int:doubt_id>', methods=['POST'])
@auth.login_required
def reply_moleDetec(pid, treNum, doubt_id):
    data = request.get_json()
    item = MoleDetec.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    if item.reply_doubt(doubt_id, data):
        return Success()
    else:
        return SampleStatusError()


