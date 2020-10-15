from flask import request

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
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
def add_immunohis(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Immunohis)
    return Success()


