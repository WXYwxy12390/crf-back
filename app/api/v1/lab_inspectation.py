"""
@author: yours
@file: lab_inspectation.py
@time: 2020-09-05 12:30
"""
from flask import request

from app.libs.decorator import edit_need_auth, update_time, record_modification
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
@update_time
@record_modification(BloodRoutine)
def add_blood_routine(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, BloodRoutine)
    return Success()


@api.route('/blood_routine/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_blood_routine(pid, treNum):
    blood_routine = BloodRoutine.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return blood_routine.submit()


@api.route('/blood_routine/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_blood_routine(pid, treNum):
    blood_routine = BloodRoutine.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return blood_routine.finish()


# 血生化的获取和提交
@api.route('/blood_bio/<int:pid>/<int:treNum>', methods=['GET'])
def get_blood_bio(pid, treNum):
    blood_bio = BloodBio.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=blood_bio if blood_bio else {})


@api.route('/blood_bio/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(BloodBio)
def add_blood_bio(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, BloodBio)
    return Success()


@api.route('/blood_bio/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_blood_bio(pid, treNum):
    blood_bio = BloodBio.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return blood_bio.submit()


@api.route('/blood_bio/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_blood_bio(pid, treNum):
    blood_bio = BloodBio.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return blood_bio.finish()


# 甲状腺的获取和提交
@api.route('/thyroid/<int:pid>/<int:treNum>', methods=['GET'])
def get_thyroid(pid, treNum):
    thyroid = Thyroid.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=thyroid if thyroid else {})


@api.route('/thyroid/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(Thyroid)
def add_thyroid(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Thyroid)
    return Success()


@api.route('/thyroid/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_thyroid(pid, treNum):
    thyroid = Thyroid.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return thyroid.submit()


@api.route('/thyroid/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_thyroid(pid, treNum):
    thyroid = Thyroid.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return thyroid.finish()


# 凝血功能的获取和提交
@api.route('/coagulation/<int:pid>/<int:treNum>', methods=['GET'])
def get_coagulation(pid, treNum):
    coagulation = Coagulation.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=coagulation if coagulation else {})


@api.route('/coagulation/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(Coagulation)
def add_coagulation(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Coagulation)
    return Success()


@api.route('/coagulation/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_coagulation(pid, treNum):
    coagulation = Coagulation.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return coagulation.submit()


@api.route('/coagulation/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_coagulation(pid, treNum):
    coagulation = Coagulation.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return coagulation.finish()


# 心肌酶谱的获取和提交
@api.route('/myocardialEnzyme/<int:pid>/<int:treNum>', methods=['GET'])
def get_myocardialEnzyme(pid, treNum):
    myocardialEnzyme = MyocardialEnzyme.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=myocardialEnzyme if myocardialEnzyme else {})


@api.route('/myocardialEnzyme/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(MyocardialEnzyme)
def add_myocardialEnzyme(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, MyocardialEnzyme)
    return Success()


@api.route('/myocardialEnzyme/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_myocardialEnzyme(pid, treNum):
    myocardialEnzyme = MyocardialEnzyme.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return myocardialEnzyme.submit()


@api.route('/myocardialEnzyme/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_myocardialEnzyme(pid, treNum):
    myocardialEnzyme = MyocardialEnzyme.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return myocardialEnzyme.finish()


# 细胞因子的获取和提交
@api.route('/cytokines/<int:pid>/<int:treNum>', methods=['GET'])
def get_cytokines(pid, treNum):
    cytokines = Cytokines.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=cytokines if cytokines else {})


@api.route('/cytokines/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(Cytokines)
def add_cytokines(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, Cytokines)
    return Success()


@api.route('/cytokines/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_cytokines(pid, treNum):
    cytokines = Cytokines.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return cytokines.submit()


@api.route('/cytokines/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_cytokines(pid, treNum):
    cytokines = Cytokines.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return cytokines.finish()


# 淋巴细胞亚群的获取和提交
@api.route('/lymSubsets/<int:pid>/<int:treNum>', methods=['GET'])
def get_lymSubsets(pid, treNum):
    lymSubsets = LymSubsets.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=lymSubsets if lymSubsets else {})


@api.route('/lymSubsets/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(LymSubsets)
def add_lymSubsets(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, LymSubsets)
    return Success()


@api.route('/lymSubsets/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_lymSubsets(pid, treNum):
    lymSubsets = LymSubsets.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return lymSubsets.submit()


@api.route('/lymSubsets/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_lymSubsets(pid, treNum):
    lymSubsets = LymSubsets.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return lymSubsets.finish()


# 尿常规获取和提交
@api.route('/urine_routine/<int:pid>/<int:treNum>', methods=['GET'])
def get_urine_routine(pid, treNum):
    urine_routine = UrineRoutine.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=urine_routine if urine_routine else {})


@api.route('/urine_routine/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(UrineRoutine)
def add_urine_routine(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, UrineRoutine)
    return Success()


@api.route('/urine_routine/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_urine_routine(pid, treNum):
    urine_routine = UrineRoutine.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return urine_routine.submit()


@api.route('/urine_routine/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_urine_routine(pid, treNum):
    urine_routine = UrineRoutine.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return urine_routine.finish()


# 肿瘤标志物获取和提交
@api.route('/tumor_marker/<int:pid>/<int:treNum>', methods=['GET'])
def get_tumor_marker(pid, treNum):
    tumor_marker = TumorMarker.query.filter_by(pid=pid, treNum=treNum).first()
    return Success(data=tumor_marker if tumor_marker else {})


@api.route('/tumor_marker/<int:pid>/<int:treNum>', methods=['POST'])
@auth.login_required
@edit_need_auth
@update_time
@record_modification(TumorMarker)
def add_tumor_marker(pid, treNum):
    data = request.get_json()
    data['pid'] = pid
    data['treNum'] = treNum
    json2db(data, TumorMarker)
    return Success()


@api.route('/tumor_marker/submit/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def submit_tumor_marker(pid, treNum):
    tumor_marker = TumorMarker.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return tumor_marker.submit()


@api.route('/tumor_marker/finish/<int:pid>/<int:treNum>', methods=['GET'])
@auth.login_required
def finish_tumor_marker(pid, treNum):
    tumor_marker = TumorMarker.query.filter_by(pid=pid, treNum=treNum).first_or_404()
    return tumor_marker.finish()
