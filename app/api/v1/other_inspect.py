"""
@author: yours
@file: other_inspect.py
@time: 2020-09-05 13:59
"""

from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models import json2db, db, delete_array
from app.models.other_inspect import Lung, OtherExams, ImageExams

api = Redprint('other_inspect')

@api.route('/lung_function/<int:pid>/<int:treNum>',methods=['GET'])
def get_lung_function(pid,treNum):
    data = Lung.query.filter_by(pid=pid,treNum=treNum).first()
    return Success(data=data if data else {})

@api.route('/lung_function/<int:pid>/<int:treNum>',methods=['POST'])
def add_lung_function(pid,treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Lung)
    return Success()



@api.route('/other_exam/<int:pid>/<int:treNum>',methods=['GET'])
def get_other_exam(pid,treNum):
    data = OtherExams.query.filter_by(pid=pid,treNum=treNum).first()
    return Success(data=data if data else {})

@api.route('/other_exam/<int:pid>/<int:treNum>',methods=['POST'])
def add_other_exam(pid,treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, OtherExams)
    return Success()


@api.route('/image_exam/<int:pid>/<int:treNum>',methods=['GET'])
def get_image_exam(pid,treNum):
    data = ImageExams.query.filter_by(pid=pid,treNum=treNum).all()
    return Success(data=data if data else [])

@api.route('/image_exam/<int:pid>/<int:treNum>',methods=['POST'])
def add_image_exam(pid,treNum):
    data = request.get_json()
    for _data in data['data']:
        _data['pid'] = pid
        _data['treNum'] = treNum
        json2db(_data, ImageExams)
    return Success()

@api.route('/image_exam/<int:pid>/<int:treNum>',methods=['DELETE'])
def del_image_exam(pid,treNum):
    data = request.get_json()
    items = ImageExams.query.filter(ImageExams.is_delete==0,ImageExams.id.in_(data['ids'])).all()
    delete_array(items)
    return Success()