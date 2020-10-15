"""
@author: yours
@file: lab_inspectation.py
@time: 2020-09-05 12:30
"""
from flask import request

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker

api = Redprint('lab_inspectation')


@api.route('/blood_routine/<int:pid>/<int:treNum>', methods=['GET'])
def get_blood_routine(pid, treNum):
    blood_routine = BloodRoutine.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=blood_routine if blood_routine else {})


@api.route('/blood_routine/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_blood_routine(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, BloodRoutine)
    return Success()


# 血生化的获取和提交
@api.route('/blood_bio/<int:pid>/<int:treNum>', methods=['GET'])
@edit_need_auth
def get_blood_bio(pid, treNum):
    blood_bio = BloodBio.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=blood_bio if blood_bio else {})


@api.route('/blood_bio/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_blood_bio(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, BloodBio)
    return Success()


# 甲状腺的获取和提交
@api.route('/thyroid/<int:pid>/<int:treNum>', methods=['GET'])
def get_thyroid(pid, treNum):
    thyroid = Thyroid.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=thyroid if thyroid else {})


@api.route('/thyroid/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_thyroid(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Thyroid)
    return Success()


# 凝血功能的获取和提交
@api.route('/coagulation/<int:pid>/<int:treNum>', methods=['GET'])
def get_coagulation(pid, treNum):
    coagulation = Coagulation.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=coagulation if coagulation else {})


@api.route('/coagulation/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_coagulation(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Coagulation)
    return Success()


# 心肌酶谱的获取和提交
@api.route('/myocardialEnzyme/<int:pid>/<int:treNum>', methods=['GET'])
def get_myocardialEnzyme(pid, treNum):
    myocardialEnzyme = MyocardialEnzyme.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=myocardialEnzyme if myocardialEnzyme else {})


@api.route('/myocardialEnzyme/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_myocardialEnzyme(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, MyocardialEnzyme)
    return Success()

# 细胞因子的获取和提交
@api.route('/cytokines/<int:pid>/<int:treNum>', methods=['GET'])
def get_cytokines(pid, treNum):
    cytokines = Cytokines.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=cytokines if cytokines else {})


@api.route('/cytokines/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_cytokines(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Cytokines)
    return Success()

# 淋巴细胞亚群的获取和提交
@api.route('/lymSubsets/<int:pid>/<int:treNum>', methods=['GET'])
def get_lymSubsets(pid, treNum):
    lymSubsets = LymSubsets.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=lymSubsets if lymSubsets else {})


@api.route('/lymSubsets/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_lymSubsets(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, LymSubsets)
    return Success()

# 尿常规获取和提交
@api.route('/urine_routine/<int:pid>/<int:treNum>', methods=['GET'])
def get_urine_routine(pid, treNum):
    urine_routine = UrineRoutine.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=urine_routine if urine_routine else {})


@api.route('/urine_routine/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_urine_routine(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, UrineRoutine)
    return Success()

# 肿瘤标志物获取和提交
@api.route('/tumor_marker/<int:pid>/<int:treNum>', methods=['GET'])
def get_tumor_marker(pid, treNum):
    tumor_marker = TumorMarker.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=tumor_marker if tumor_marker else {})


@api.route('/tumor_marker/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_tumor_marker(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, TumorMarker)
    return Success()
