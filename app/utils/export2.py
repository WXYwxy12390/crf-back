from flask import make_response
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from app.models.therapy_record import TreRec
from app.utils.date import get_birth_date_by_id_card, get_age_by_birth


class Export:
    lab_inspectation_table = ['BloodRoutine', 'BloodBio', 'Thyroid', 'Coagulation', 'MyocardialEnzyme',
                              'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker']
    other_inspect_table = ['Lung', 'OtherExams', 'ImageExams']
    header_map = {'patNumber': '编号', 'idNumber': '身份证号', 'patientName': '姓名', 'hospitalNumber': '住院号',
                  'gender': '性别', 'birthday': '出生日期', 'age': '年龄', 'phoneNumber1': '电话号码1',
                  'phoneNumber2': '电话号码2', 'updateTime': '更新时间', 'nextFollowupTime': '随访时间', 'finishFollowup': '是否完成随访',
                  'basDisHis': '基础疾病史', 'infDisHis': '传染疾病史', 'tumor': '是否有肿瘤史', 'tumHis': '肿瘤史',
                  'tumorFam': '是否有肿瘤家族史', 'tumFamHis': '肿瘤家族史', 'smoke': '是否吸烟', 'smokingHis': '吸烟史',
                  'drink': '是否饮酒', 'drinkingHis': '饮酒史', 'hormone': '是否长期使用激素', 'hormoneUseHis': '激素使用史',
                  'drug': '是否长期使用药物', 'drugUseHis': '药物使用史', 'PSScore': 'PS评分', 'cliniManifest': '临床表现',
                  'videography': '影像学', 'part': '部位', 'bioMet': '活检方式', 'pleInv': '是否胸膜侵犯',
                  'speSite': '标本部位', 'firVisDate': '初诊日期', 'patReDate': '病理报告日期', 'patNum': '病理号',
                  'patDia': '病理诊断', 'mitIma': '核分裂像', 'comCar': '复合性癌', 'necArea': '坏死面积',
                  'massSize': '肿块大小', 'Ki67': 'Ki67', 'traSite': '转移部位', 'TSize': 'TSize', 'stage': '分期情况',
                  'cliStage': '临床分期', 'patStage': '病理分期', 'cRemark': 'cRemark', 'pRemark': 'pRemark',
                  'samplingTime': '采样时间',
                  'detectTime': '检测时间', 'FVC_exp': '用力肺活量(L)预期值', 'FEV1_FVC_exp': '用力呼气一秒率(%)预期值',
                  'MEF_exp': '用力呼气中期流速(L/S)预期值', 'MEF25_exp': '25%用力呼气流速(L/S)预期值', 'MEF50_exp': '50%用力呼气流速(L/S)预期值',
                  'MEF75_exp': '75%用力呼气流速(L/S)预期值', 'TLC_sb_exp': '肺总量(L)预期值', 'RV_exp': '残气容积(L)预期值',
                  'RV_TLC_exp': '残气容积/肺总量比(%)预期值', 'VC_exp': '肺活量(L)预期值', 'DLCO_ex_exp': '无需屏气弥散(mL/mmHg/Mi)预期值',
                  'DLCO_sb_exp': '肺一氧化碳弥散量(mL/mmHg/Mi)预期值', 'KCO_exp': '比弥散量预期值', 'FVC_best': '用力肺活量(L)最佳值',
                  'FEV1_FVC_best': '用力呼气一秒率(%)最佳值', 'MEF_best': '用力呼气中期流速(L/S)最佳值', 'MEF25_best': '25%用力呼气流速(L/S)最佳值',
                  'MEF50_best': '50%用力呼气流速(L/S)最佳值', 'MEF75_best': '75%用力呼气流速(L/S)最佳值', 'TLC_sb_best': '肺总量(L)最佳值',
                  'RV_best': '残气容积(L)最佳值', 'RV_TLC_best': '残气容积/肺总量比(%)最佳值', 'VC_best': '肺活量(L)最佳值',
                  'DLCO_ex_best': '无需屏气弥散(mL/mmHg/Mi)最佳值',
                  'DLCO_sb_best': '肺一氧化碳弥散量(mL/mmHg/Mi)最佳值', 'KCO_best': '比弥散量最佳值', 'FVC_ratio': '用力肺活量(L)最佳值/预期值(%)',
                  'FEV1_FVC_ratio': '用力呼气一秒率(%)最佳值/预期值(%)', 'MEF_ratio': '用力呼气中期流速(L/S)最佳值/预期值(%)',
                  'MEF25_ratio': '25%用力呼气流速(L/S)最佳值/预期值(%)', 'MEF50_ratio': '50%用力呼气流速(L/S)最佳值/预期值(%)',
                  'MEF75_ratio': '75%用力呼气流速(L/S)最佳值/预期值(%)', 'TLC_sb_ratio': '肺总量(L)最佳值/预期值(%)',
                  'RV_ratio': '残气容积(L)最佳值/预期值(%)',
                  'RV_TLC_ratio': '残气容积/肺总量比(%)最佳值/预期值(%)', 'VC_ratio': '肺活量(L)最佳值/预期值(%)',
                  'DLCO_ex_ratio': '无需屏气弥散(mL/mmHg/Mi)最佳值/预期值(%)',
                  'DLCO_sb_ratio': '肺一氧化碳弥散量(mL/mmHg/Mi)最佳值/预期值(%)', 'KCO_ratio': '比弥散量最佳值/预期值(%)',
                  'ECGDetTime': '12导联心电图检测时间', 'ECGDesc': '12导联心电图结果描述', 'ECGPath': '12导联心电图报告路径',
                  'UCGDetTime': '超声心动图检测时间', 'UCGDesc': '超声心动图结果描述', 'UCGPath': '超声心动图报告路径',
                  'detectTime': '检测时间', 'examArea': '检查部位', 'exmaMethod': '检查方法', 'tumorLD': '肿瘤长径', 'tumorSD': '肿瘤短径',
                  'tumorDesc': '肿瘤描述', 'path': '文件路径',
                  'other': '其他', 'filePath': '文件路径', 'PDL1': 'PD-L1表达水平', 'PDL1KT': 'PDL1抗体'

                  }
    patDia_map = {
        "0-0": "上皮型肿瘤",
        "0-0-0": "上皮型肿瘤-腺癌",
        "0-0-0-0": "上皮型肿瘤-腺癌-贴壁型腺癌",
        "0-0-0-1": "上皮型肿瘤-腺癌-腺泡型腺癌",
        "0-0-0-2": "上皮型肿瘤-腺癌-乳头型腺癌",
        "0-0-0-3": "上皮型肿瘤-腺癌-微乳头型腺癌",
        "0-0-0-4": "上皮型肿瘤-腺癌-实体型腺癌",
        "0-0-0-5": "上皮型肿瘤-腺癌-浸润性粘液腺癌",
        "0-0-0-5-0": "上皮型肿瘤-腺癌-浸润性粘液腺癌-浸润和非浸润性混合型粘液性腺癌",
        "0-0-0-6": "上皮型肿瘤-腺癌-胶质性腺癌",
        "0-0-0-7": "上皮型肿瘤-腺癌-胎儿型腺癌",
        "0-0-0-8": "上皮型肿瘤-腺癌-肠型腺癌",
        "0-0-0-9": "上皮型肿瘤-腺癌-微小浸润性腺癌",
        "0-0-0-9-0": "上皮型肿瘤-腺癌-微小浸润性腺癌-非粘液性腺癌",
        "0-0-0-9-1": "上皮型肿瘤-腺癌-微小浸润性腺癌-粘液癌",
        "0-0-0-10": "上皮型肿瘤-腺癌-侵袭前病变",
        "0-0-0-10-0": "上皮型肿瘤-腺癌-侵袭前病变-非典型腺瘤样增生",
        "0-0-0-10-1": "上皮型肿瘤-腺癌-侵袭前病变-原位腺癌",
        "0-0-0-10-1-0": "上皮型肿瘤-腺癌-侵袭前病变-原位腺癌-非粘液性原位腺癌",
        "0-0-0-10-1-1": "上皮型肿瘤-腺癌-侵袭前病变-原位腺癌-粘液性原位腺癌",
        "0-0-1": "上皮型肿瘤-鳞癌",
        "0-0-1-0": "上皮型肿瘤-鳞癌-角化型鳞癌",
        "0-0-1-1": "上皮型肿瘤-鳞癌-非角化型鳞癌",
        "0-0-1-2": "上皮型肿瘤-鳞癌-基底鳞状细胞癌",
        "0-0-1-3": "上皮型肿瘤-鳞癌-侵袭前病变",
        "0-0-1-3-0": "上皮型肿瘤-鳞癌-侵袭前病变-鳞状细胞原位癌",
        "0-1": "神经内分泌肿瘤",
        "0-1-0": "神经内分泌肿瘤-小细胞癌",
        "0-1-0-0": "神经内分泌肿瘤-小细胞癌-结合小细胞癌",
        "0-1-1": "神经内分泌肿瘤-大细胞神经内分泌癌",
        "0-1-1-0": "神经内分泌肿瘤-大细胞神经内分泌癌-结合大细胞神经内分泌癌",
        "0-1-2": "神经内分泌肿瘤-类癌肿瘤",
        "0-1-2-0": "神经内分泌肿瘤-类癌肿瘤-典型类癌肿瘤",
        "0-1-2-1": "神经内分泌肿瘤-类癌肿瘤-非典型类癌肿瘤",
        "0-1-3": "神经内分泌肿瘤-侵袭前的病变",
        "0-1-3-0": "神经内分泌肿瘤-侵袭前的病变-弥漫性特发性肺神经内分泌细胞增生",
        "0-1-4": "神经内分泌肿瘤-大细胞癌",
        "0-1-5": "神经内分泌肿瘤-腺鳞癌",
        "0-1-6": "神经内分泌肿瘤-癌肉瘤样癌",
        "0-1-6-0": "神经内分泌肿瘤-癌肉瘤样癌-多形性癌",
        "0-1-6-1": "神经内分泌肿瘤-癌肉瘤样癌-梭形细胞癌",
        "0-1-6-2": "神经内分泌肿瘤-癌肉瘤样癌-巨细胞癌",
        "0-1-6-3": "神经内分泌肿瘤-癌肉瘤样癌-癌肉瘤",
        "0-1-6-4": "神经内分泌肿瘤-癌肉瘤样癌-肺胚细胞瘤",
        "0-1-7": "神经内分泌肿瘤-其他未分类癌",
        "0-1-7-0": "神经内分泌肿瘤-其他未分类癌-淋巴上皮样癌",
        "0-1-7-1": "神经内分泌肿瘤-其他未分类癌-NUT肿瘤",
        "0-1-8": "神经内分泌肿瘤-唾液型肿瘤",
        "0-1-8-0": "神经内分泌肿瘤-唾液型肿瘤-粘液表皮样癌肿瘤",
        "0-1-8-1": "神经内分泌肿瘤-唾液型肿瘤-腺样囊性癌",
        "0-1-8-2": "神经内分泌肿瘤-唾液型肿瘤-上皮-肌上皮癌",
        "0-1-8-3": "神经内分泌肿瘤-唾液型肿瘤-多形性腺瘤",
        "0-1-9": "神经内分泌肿瘤-乳头状瘤",
        "0-1-9-0": "神经内分泌肿瘤-乳头状瘤-鳞状细胞乳头状癌",
        "0-1-9-0-0": "神经内分泌肿瘤-乳头状瘤-鳞状细胞乳头状癌-外生型",
        "0-1-9-0-1": "神经内分泌肿瘤-乳头状瘤-鳞状细胞乳头状癌-逆向生长",
        "0-1-9-1": "神经内分泌肿瘤-乳头状瘤-腺型状瘤",
        "0-1-9-2": "神经内分泌肿瘤-乳头状瘤-腺鳞混合型乳头状瘤",
        "0-1-10": "神经内分泌肿瘤-腺瘤",
        "0-1-10-0": "神经内分泌肿瘤-腺瘤-良性硬化性肺细胞瘤",
        "0-1-10-1": "神经内分泌肿瘤-腺瘤-泡腺腺瘤",
        "0-1-10-2": "神经内分泌肿瘤-腺瘤-乳头状腺瘤",
        "0-1-10-3": "神经内分泌肿瘤-腺瘤-粘液性囊腺瘤腺瘤",
        "0-1-10-4": "神经内分泌肿瘤-腺瘤-粘液腺腺瘤",
        "0-2": "间叶性肿瘤",
        "0-2-0": "间叶性肿瘤-肺错构瘤",
        "0-2-1": "间叶性肿瘤-软骨瘤",
        "0-2-2": "间叶性肿瘤-PEComatous肿瘤",
        "0-2-2-0": "间叶性肿瘤-PEComatous肿瘤-淋巴管平滑肌瘤病",
        "0-2-2-1": "间叶性肿瘤-PEComatous肿瘤-PEComa-良性",
        "0-2-2-1-0": "间叶性肿瘤-PEComatous肿瘤-PEComa-良性-透明细胞瘤",
        "0-2-2-2": "间叶性肿瘤-PEComatous肿瘤-PEComa-恶性",
        "0-2-3": "间叶性肿瘤-先天性支气管周肌纤维母细胞肿瘤",
        "0-2-4": "间叶性肿瘤-弥漫性肺淋巴管瘤病",
        "0-2-5": "间叶性肿瘤-炎症性肌纤维母细胞瘤",
        "0-2-6": "间叶性肿瘤-上皮样血管内皮瘤",
        "0-2-7": "间叶性肿瘤-胸膜肺母细胞瘤",
        "0-2-8": "间叶性肿瘤-滑膜肉瘤",
        "0-2-9": "间叶性肿瘤-肺动脉内膜肉瘤",
        "0-2-10": "间叶性肿瘤-肺黏液肉瘤伴EWSR1-CREB1易位",
        "0-2-11": "间叶性肿瘤-肌上皮肿瘤",
        "0-2-11-0": "间叶性肿瘤-肌上皮肿瘤-肌上皮瘤",
        "0-2-11-1": "间叶性肿瘤-肌上皮肿瘤-肌上皮癌",
        "0-2-12": "间叶性肿瘤-淋巴细胞组织细胞肿瘤",
        "0-2-13": "间叶性肿瘤-结外边缘区黏膜相关淋巴组织淋巴瘤（MALT淋巴瘤）",
        "0-2-14": "间叶性肿瘤-弥漫性大细胞淋巴瘤",
        "0-2-15": "间叶性肿瘤-淋巴瘤样肉芽肿",
        "0-2-16": "间叶性肿瘤-血管内大B细胞淋巴瘤",
        "0-2-17": "间叶性肿瘤-肺朗格罕细胞组织细胞增生症",
        "0-2-18": "间叶性肿瘤-Erdheim-Chester病",
        "0-3": "异位肿瘤",
        "0-3-0": "异位肿瘤-生殖细胞肿瘤",
        "0-3-0-0": "异位肿瘤-生殖细胞肿瘤-畸胎瘤-成熟",
        "0-3-0-1": "异位肿瘤-生殖细胞肿瘤-畸胎瘤-不成熟",
        "0-3-1": "异位肿瘤-肺内的胸腺瘤",
        "0-3-2": "异位肿瘤-黑色素瘤",
        "0-3-3": "异位肿瘤-脑膜瘤",
        "0-4": "转移性肿瘤",
        "0-5": "其他"
    }  # 病理诊断map
    gender_map = {0: "女", 1: "男", "/": "/"}
    immunohis_map = {0: '-', 1: '±', 2: '+', 3: '++', 4: '+++'}
    moleDetec_map = {0: '阴性', 1: '阳性', 2: '无'}

    def __init__(self, info, tables, columns):
        self.headers = []
        self.info = info
        self.tables = tables
        self.columns = columns
        i = 0
        for x in columns:
            name = tables[i].__name__
            if (name in self.lab_inspectation_table or
                    name == 'Immunohis' or name == 'MoleDetec'):
                for y in x:
                    if (y == 'samplingTime' or y == 'other' or y == 'filePath' or
                            y == 'PDL1' or y == 'PDL1KT'):
                        self.headers.append(self.header_map.get(y))
                    else:
                        self.headers.append(y)

            else:
                for y in x:
                    if y == 'cStage':
                        self.headers.append('c分期T')
                        self.headers.append('c分期N')
                        self.headers.append('c分期M')
                    elif y == 'pStage':
                        self.headers.append('p分期T')
                        self.headers.append('p分期N')
                        self.headers.append('p分期M')
                    else:
                        self.headers.append(self.header_map.get(y))
            i += 1

    def work(self):
        wb = Workbook()
        ws = wb.active
        ws.title = '导出样本数据'
        ws.append(self.headers)

        for dic in self.info:
            row = []
            i = 0
            pid = dic.get('pid')
            treNum = dic.get('treNum')
            for obj_class_name in self.tables:
                name = obj_class_name.__name__
                if name == 'Patient':
                    obj_array = obj_class_name.query.filter(obj_class_name.id == pid,
                                                            obj_class_name.is_delete == 0).all()
                elif name == 'PastHis' or name == 'IniDiaPro':
                    obj_array = obj_class_name.query.filter(obj_class_name.pid == pid,
                                                            obj_class_name.is_delete == 0).all()
                elif (name in self.lab_inspectation_table or name in self.other_inspect_table or
                      name == 'Immunohis' or name == 'MoleDetec'):
                    obj_array = obj_class_name.query.filter(obj_class_name.pid == pid,
                                                            obj_class_name.treNum == treNum,
                                                            obj_class_name.is_delete == 0).all()
                if obj_array:
                    obj = obj_array[0]
                    for field in self.columns[i]:
                        if field != 'age':
                            x = getattr(obj, field)

                        if name == 'Immunohis':
                            value = self.filter_none(obj, field)
                            value = self.immunohis_map.get(value)
                        elif name == 'MoleDetec':
                            value = self.filter_none(obj, field)
                            value = self.moleDetec_map.get(value)
                        elif field == 'gender':
                            value = self.filter_none(obj, field)
                            value = self.gender_map.get(value)
                        elif field == 'age':
                            idNumber = getattr(obj, 'idNumber')
                            age = get_age_by_birth(get_birth_date_by_id_card(idNumber))
                            value = age if age else '/'
                        elif field == 'drinkingHis':
                            value = self.format_drink_history(obj)
                        elif field == 'smokingHis':
                            value = self.format_smoke_history(obj)
                        elif field == 'cStage' or field == 'pStage':
                            stage_array = self.format_stage(obj, field)
                            row.extend(stage_array)
                        elif (field == 'bioMet' or field == 'traSite' or
                              field == 'basDisHis' or field == 'infDisHis' or
                              field == 'tumHis' or field == 'tumFamHis' or
                              field == 'cliniManifest' or field == 'part'):
                            value = self.format_radio_data(obj, field)
                        elif field == 'patDia':
                            value = self.format_patDia(obj)
                        elif type(x) == bool:
                            value = self.filter_none(self.change_bool_to_yes_or_no(x))
                        elif type(x) == dict:
                            value = str(x) if x else '/'
                        elif type(x) == list:
                            value = str(x) if x else '/'
                        else:
                            value = self.filter_none(obj, field)

                        if field != 'cStage' and field != 'pStage':
                            row.append(value)
                else:
                    for j in range(0, len(self.columns[i])):
                        row.append('/')

                i += 1
            ws.append(row)

        wb.save('test.xlsx')
        content = save_virtual_workbook(wb)
        resp = make_response(content)
        resp.headers["Content-Disposition"] = 'attachment; filename=samples.xlsx'
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp






    def change_bool_to_yes_or_no(self, bool_value):
        if bool_value is None:
            return '/'
        return '是' if bool_value else '否'

    def filter_none(self, data, item=None):
        if data is None:
            return '/'
        if item:
            val = getattr(data, item)
        else:
            val = data
        return val if val is not None else '/'

    def format_smoke_history(self, object):
        if object is None:
            return '/'
        is_smoke = object.smoke
        info = object.smokingHis
        value = '/'
        if is_smoke == 1:
            value = '累积吸烟时间（年）' + str(info.get('smokeYearAvg')) + '日平均吸烟量（支）' + str(info.get('smokeDayAvg'))
        elif is_smoke == 0:
            value = '无'
        return value

    def format_drink_history(self, object):
        if object is None:
            return '/'
        is_drink = object.drink
        info = object.drinkingHis
        value = '/'
        if is_drink == 1:
            value = '累积饮酒时间（年）' + str(info.get('drinkYearAvg')) + '日平均饮酒量（mL）' + str(info.get('drinkDayAvg'))
        elif is_drink == 0:
            value = '无'
        return value

    def format_radio_data(self, object, item):
        if object is None:
            return '/'
        data = getattr(object, item)
        if data is None:
            return '/'
        radio = data.get('radio')
        other = data.get('other')
        value = ",".join(radio)
        if other:
            value = value + "," + "其他: " + other
        return value

    def format_patDia(self, object):
        if object is None or object.patDia is None:
            return '/'
        patDia = object.patDia
        radio = patDia.get('radio')
        data = []
        for item in radio:
            if item != "0-5":
                data.append(self.patDia_map.get(item))
            else:
                data.append("其他：" + str(patDia.get('other')))
        return ','.join(data)

    def format_stage(self, object, item):
        value = ['/'] * 3
        if object is None:
            return value
        data = getattr(object, item)
        if data is None or data == "":
            return value
        ret = data.split(',')
        for i in range(0, 3):
            value[i] = self.filter_none(ret[i])
        return value
