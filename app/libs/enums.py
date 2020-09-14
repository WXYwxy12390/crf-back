from enum import Enum


class SampleStatus(Enum):
    # 样本提交状态
    NotSubmit = 0
    SubSubmit = 1
    AllSubmit = 2
    Unlock = 3

class LesionStatus(Enum):
    Progress = 3



interface_dict = {
    "v1.adverse_event+add_adverse_event":'不良事件',"v1.adverse_event+del_adverse_event":'不良事件',
    "v1.concomitant_medication+add_concomitant_medication":'伴随用药',"v1.concomitant_medication+del_concomitant_medication":'伴随用药',

    'v1.criteria+add_inclusion_criteria':'入组筛选-入选标准', 'v1.criteria+add_exclusion_criteria':'入组筛选-排除标准',

    'v1.cycle+add_cycle_status':'访视完成情况',

    'v1.demography+add_demography':"人口学资料",
    'v1.ecog+add_ecog':"ECOG评分",

    'v1.effect_evaluation+add_targeted_lesion':'肿瘤疗效评估-靶病灶','v1.effect_evaluation+del_targeted_lesion':'肿瘤疗效评估-靶病灶',
    'v1.effect_evaluation+add_not_targeted_lesion':'肿瘤疗效评估-非靶病灶','v1.effect_evaluation+del_not_targeted_lesion':'肿瘤疗效评估-非靶病灶',
    'v1.effect_evaluation+add_new_lesion':'肿瘤疗效评估-新病灶','v1.effect_evaluation+del_new_lesion':'肿瘤疗效评估-新病灶',
    'v1.effect_evaluation+add_not_new_lesion':'肿瘤疗效评估-新非病灶','v1.effect_evaluation+del_not_new_lesion':'肿瘤疗效评估-新非病灶',



    'v1.lab_inspection+add_blood_routine':'实验室检查-血常规','v1.lab_inspection+del_blood_routine':'实验室检查-血常规',
    'v1.lab_inspection+add_blood_biochemistry':'实验室检查-血生化',
    'v1.lab_inspection+add_blood_clotting':'实验室检查-凝血功能',
    'v1.lab_inspection+add_thyroid_function':'实验室检查-甲状腺',
    'v1.lab_inspection+add_myocardial_enzyme':'实验室检查-心肌酶谱',
    'v1.lab_inspection+add_AMY':'实验室检查-血清淀粉酶AMY',
    'v1.lab_inspection+add_LPS':'实验室检查-脂肪酶',
    'v1.lab_inspection+add_tumor_marker':'实验室检查-肿瘤标记物',
    'v1.lab_inspection+add_virus_indicator':'实验室检查-病毒学指标',
    'v1.lab_inspection+add_HCG':'实验室检查-育龄妇女血清HCG',
    'v1.lab_inspection+add_urinalysis':'实验室检查-尿常规','v1.lab_inspection+del_urinalysis':'实验室检查-尿常规',
    'v1.lab_inspection+add_shit_routine':'实验室检查-大便常规',


    'v1.medicine_usage_research+add_medicine_usage_research':'研究用药','v1.medicine_usage_research+del_medicine_usage_research':'研究用药',

    'v1.other_inspect+add_12_lead_ecg':'其他检查-12导联心动图',
    'v1.other_inspect+add_UCG':'其他检查-超声心动图',
    'v1.other_inspect+add_photo_inspect':'其他检查-影像学检查','v1.other_inspect+del_photo_inspect':'其他检查-影像学检查',
    'v1.other_inspect+add_lung_function':'其他检查-肺功能',

    'v1.other_tumor_therapy+add_other_tumor_therapy':'后续其他抗肿瘤治疗','v1.other_tumor_therapy+del_other_tumor_therapy':'后续其他抗肿瘤治疗',

    'v1.past_history+add_smoke_drink_history':"既往史-烟酒史",
    'v1.past_history+add_lung_cancer_histroy':'既往史-肺癌病史',
    'v1.past_history+add_lung_cancer_therapy_histroy':'既往史-肺癌病史-肺癌既往治疗史','v1.past_history+del_lung_cancer_therapy_histroy':'既往史-肺癌病史-肺癌既往治疗史',
    'v1.past_history+add_lung_cancer_past_disease':'既往史-肺癌病史-既往伴随病史','v1.past_history+del_lung_cancer_past_disease':'既往史-肺癌病史-既往伴随病史',

    'v1.QoL+add_QoL':'QoL量表',

    'v1.relative_inspect+add_relative_inspect':'相关检查','v1.relative_inspect+del_relative_inspect':'相关检查',
    'v1.stop_modify_dose+add_stop_modify_dose':'停药/剂量调整','v1.stop_modify_dose+del_stop_modify_dose':'停药/剂量调整',

    'v1.summary+add_summary':'项目总结',
    'v1.survival_cycle+add_survival_cycle':'生存随访',
    'v1.survival_cycle+add_disease_progress_or_die_date_record':'疾病进展/死亡时间记录',

    'v1.physical_examination+add_physical_examination':'体格检查',
    'v1.vital_sign+add_vital_sign':'生命体征',
    'v1.vital_sign+add_blood_pressure':'血压监测','v1.vital_sign+del_blood_pressure':'血压监测',

}