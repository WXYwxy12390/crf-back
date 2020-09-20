from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, delete_array
from app.models.cycle import Signs, SideEffect
from app.models.therapy_record import TreRec
from app.utils.date import str2date

api = Redprint('treatment_info')


# 疗效评估的获取和提交
@api.route('/evaluation/<int:pid>/<int:treNum>/<int:trement>', methods=['GET'])
def get_treatment_evaluation(pid, treNum, trement):
    treRec = TreRec.query.filter_by(pid=pid, treNum=treNum, trement=trement).first()
    return Success(data=treRec if treRec else {})


@api.route('/evaluation/<int:pid>/<int:treNum>/<int:trement>', methods=['POST'])
def add_treatment_evaluation(pid, treNum, trement):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    data['trement'] = trement
    json2db(data, TreRec)
    return Success()

# 症状体征的获取、提交、删除
@api.route('/signs/<int:pid>/<int:treNum>', methods=['GET'])
def get_signs(pid, treNum):
    signs = Signs.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=signs if signs else {})


@api.route('/signs/<int:pid>/<int:treNum>', methods=['POST'])
def add_signs(pid, treNum):
    data = request.get_json()
    for _data in data:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, Signs)
    return Success()


@api.route('/signs/<int:sign_id>',methods=['DELETE'])
def del_signs(sign_id):
    sign = Signs.query.filter_by(id=sign_id).all()
    delete_array(sign)
    return Success()

# 副反应的获取、提交、删除
@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['GET'])
def get_side_effect(pid, treNum):
    side_effect = SideEffect.query.filter_by(pid=pid, treNum=treNum).all()
    return Success(data=side_effect if side_effect else {})


@api.route('/side_effect/<int:pid>/<int:treNum>', methods=['POST'])
def add_side_effect(pid, treNum):
    data = request.get_json()
    for _data in data:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, SideEffect)
    return Success()


@api.route('/side_effect/<int:se_id>',methods=['DELETE'])
def del_side_effect(se_id):
    side_effect = SideEffect.query.filter_by(id=se_id).all()
    delete_array(side_effect)
    return Success()
