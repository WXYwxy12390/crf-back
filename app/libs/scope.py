class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    # 运算符重载  实现对象和对象直接相加
    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))  # 转成集合去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))  # 转成集合去重

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))  # 转成集合去重

        return self  # 返回实例对象，使其能够支持链式调用


# class AdminScope(Scope):
#     #allow_api = ['v1.super_get_user']
#     allow_module = ['v1.user']
#
# class UserScope(Scope):
#     #allow_api = []
#     forbidden = ['v1.user+super_get_user','v1.user+super_delete_user']
#
#     def __init__(self):
#         self + AdminScope()
#
#
# class SuperScope(Scope):
#     allow_api = []
#     def __init__(self):
#         #通过运算符重载，实现了 干净的代码--舒服
#         self +  UserScope()+ AdminScope()

class OperateUserCRF(Scope):
    allow_api = ['v1.sample+add_sample', 'v1.sample+get_sample_all', 'v1.sample+get_sample_updated',
                 'v1.sample+sample_add_account',
                 'v1.modification+submit_cycle', 'v1.modification+submit',
                 'v1.modification+reply', 'v1.modification+get_history'
                 ]
    allow_module = ['v1.first_diagnose', 'v1.past_history', 'v1.patient', 'v1.record_info', 'v1.therapy_record',
                    'v1.file', 'v1.immunohis', 'v1.lab_inspectation', 'v1.mole_detec', 'v1.other_inspect',
                    'v1.treatment_info', 'v1.specimen_info',
                    'v1.user']


class CheckCenterCRF(Scope):
    allow_api = ['v1.sample+get_sample_all', 'v1.sample+get_sample_updated']


class EditCenterCRF(Scope):
    def __init__(self):
        self + OperateUserCRF()


class OperateAllCRF(Scope):
    def __init__(self):
        self + OperateUserCRF()


class DeleteCRF(Scope):
    allow_api = ['v1.sample+del_sample']


class Export(Scope):
    # 导出
    allow_api = []


class InputCRF(Scope):
    # 8 多中心录入CRF
    allow_module = ['v1.adverse_event', 'v1.concomitant_medication', 'v1.criteria', 'v1.cycle', 'v1.demography',
                    'v1.ecog',
                    'v1.effect_evaluation', 'v1.file', 'v1.lab_inspection', 'v1.medicine_usage_research',
                    'v1.other_inspect', 'v1.other_tumor_therapy', 'v1.past_history', 'v1.physical_examination',
                    'v1.QoL',
                    'v1.relative_inspect', 'v1.sample', 'v1.stop_modify_dose', 'v1.summary', 'v1.survival_cycle',
                    'v1.vital_sign',
                    'v1.action_record', 'v1.specimen_info'
                    ]


class CheckCRF(Scope):
    allow_api = ["v1.adverse_event+get_adverse_event",
                 "v1.concomitant_medication+get_concomitant_medication",
                 'v1.criteria+get_inclusion_criteria', 'v1.criteria+get_exclusion_criteria',
                 'v1.cycle+get_cycle_nav', 'v1.cycle+get_cycle_info', 'v1.cycle+get_cycle_status',
                 'v1.demography+get_demography',
                 'v1.ecog+get_ecog',
                 'v1.effect_evaluation+get_effect_evaluation', 'v1.effect_evaluation+get_targeted_lesion',
                 'v1.effect_evaluation+get_not_targeted_lesion', 'v1.effect_evaluation+get_new_lesion',
                 'v1.effect_evaluation+get_not_new_lesion',
                 'v1.file+get_signiture_path', 'v1.file+get_file',

                 'v1.lab_inspection+get_blood_routine', 'v1.lab_inspection+get_blood_biochemistry',
                 'v1.lab_inspection+get_blood_clotting',
                 'v1.lab_inspection+get_thyroid_function', 'v1.lab_inspection+get_myocardial_enzyme',
                 'v1.lab_inspection+get_AMY',
                 'v1.lab_inspection+get_LPS', 'v1.lab_inspection+get_tumor_marker',
                 'v1.lab_inspection+get_virus_indicator',
                 'v1.lab_inspection+get_HCG', 'v1.lab_inspection+get_urinalysis', 'v1.lab_inspection+get_shit_routine',

                 'v1.medicine_usage_research+get_medicine_usage_research',
                 'v1.other_inspect+get_12_lead_ecg', 'v1.other_inspect+get_UCG', 'v1.other_inspect+get_photo_inspect',
                 'v1.other_inspect+get_lung_function',
                 'v1.other_tumor_therapy+get_other_tumor_therapy',
                 'v1.past_history+get_smoke_drink_history', 'v1.past_history+get_lung_cancer_histroy',
                 'v1.past_history+get_lung_cancer_therapy_histroy', 'v1.past_history+get_lung_cancer_past_disease',
                 'v1.physical_examination+get_physical_examination',
                 'v1.QoL+get_QoL', 'v1.QoL+get_Qol_C30_result', 'v1.QoL+get_Qol_LC13_result',
                 'v1.relative_inspect+get_relative_inspect',
                 'v1.sample+get_sample_all',
                 'v1.stop_modify_dose+get_stop_modify_dose',
                 'v1.summary+get_summary', 'v1.summary+get_adverse_event_table',
                 'v1.survival_cycle+get_survival_cycle', 'v1.survival_cycle+get_disease_progress_or_die_date_record',
                 'v1.vital_sign+get_vital_sign', 'v1.vital_sign+get_blood_pressure',
                 'v1.action_record+get_unlock_record'
                 ]


# 能够查看全部样本
class CheckAllCrf(Scope):
    forbidden = []


# 统计分析
class Analysis(Scope):
    forbidden = []


# 查看编辑所有标本信息
class OperateAllSpeciInfo(Scope):
    allow_api = ['v1.sample+add_sample']
    allow_module = ['v1.specimen_info']


class CRA(Scope):
    allow_api = ['v1.modification+begin_monitor', 'v1.modification+finish',
                 'v1.modification+doubt']


# 这里的endpoint 会带有蓝图v1 例如  v1.super_get_user
def is_in_scope(scopes, endpoint):
    # endpoint = blueprint.view_function
    # globals() 实现'反射'
    # globals 会将当前模块下的类转换为字典
    # scope = globals()[scope]() #根据scope 实例化一个权限对象scope
    scope = Scope()
    for scopeStr in scopes:
        scope += globals()[scopeStr]()
    # 分离出 模块名，以便进行模块级别的验证
    splits = endpoint.split('+')
    red_name = splits[0]

    if endpoint in scope.forbidden:
        return False

    if endpoint in scope.allow_api:
        return True

    if red_name in scope.allow_module:
        return True
    else:
        return False
