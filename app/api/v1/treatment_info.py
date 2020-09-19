from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db
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
    if data.get('beEffEvaDate') is not None:
        data['beEffEvaDate'] = str2date(data['beEffEvaDate'])
    if data.get('proDate') is not None:
        data['proDate'] = str2date(data['proDate'])
    json2db(data, TreRec)
    return Success()
