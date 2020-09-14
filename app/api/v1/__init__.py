from flask import Blueprint
from app.api.v1 import user, client, token #直接导入模块，可以避免导入api重名的问题
from app.api.v1.base_line import patient,past_history
from app.api.v1 import lab_inspectation,other_inspect

#把红图注册到蓝图下
def create_blueprint_v1():
    bp_v1 = Blueprint('v1',__name__,static_folder='../../static')
    # user.api.register(bp_v1) #利用红图注册到蓝图上
    # client.api.register(bp_v1)
    # token.api.register(bp_v1)
    patient.api.register(bp_v1)
    past_history.api.register(bp_v1)
    lab_inspectation.api.register(bp_v1)
    other_inspect.api.register(bp_v1)
    return bp_v1
