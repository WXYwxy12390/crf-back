from flask import request

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
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
def add_mole_detec(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, MoleDetec)
    return Success()


