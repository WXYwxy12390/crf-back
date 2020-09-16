"""
@author: yours
@file: therapy_record.py
@time: 2020-09-14 21:52
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.therapy_record import TreRec

api = Redprint('therapy_record')

@api.route('/<int:pid>/<int:treNum>',methods = ['GET'])
def get_therapy_record(pid,treNum):
    tre_rec = TreRec.query.filter_by(pid=pid,treNum=treNum).first()
    return Success(data=tre_rec if tre_rec else {})

