from flask import Blueprint
from app.api.v1 import user, client, token, immunohis, mole_detec, treatment_info  # 直接导入模块，可以避免导入api重名的问题
from app.api.v1.base_line import patient, past_history, first_diagnose, specimen_info
from app.api.v1 import lab_inspectation, other_inspect
from app.api.v1.record_info import record_info, therapy_record
from app.api.v1 import sample, file, migrate, export


# 把红图注册到蓝图下
def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__, static_folder='../../static')
    user.api.register(bp_v1)  # 利用红图注册到蓝图上
    # client.api.register(bp_v1)
    # token.api.register(bp_v1)
    patient.api.register(bp_v1)
    past_history.api.register(bp_v1)
    lab_inspectation.api.register(bp_v1)
    other_inspect.api.register(bp_v1)
    first_diagnose.api.register(bp_v1)
    record_info.api.register(bp_v1)
    therapy_record.api.register(bp_v1)
    sample.api.register(bp_v1)
    immunohis.api.register(bp_v1)
    mole_detec.api.register(bp_v1)
    treatment_info.api.register(bp_v1)
    file.api.register(bp_v1)
    migrate.api.register(bp_v1)
    export.api.register(bp_v1)
    specimen_info.api.register(bp_v1)
    return bp_v1
