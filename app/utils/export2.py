from flask import make_response
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from app.utils.date import get_birth_date_by_id_card, get_age_by_birth


class Export:

    header_map = {'patNumber': '编号', 'idNumber': '身份证号', 'patientName': '姓名',
                 'gender': '性别', 'birthday': '出生年月', 'age': '年龄', 'phoneNumber1': '电话号码',
                 'PSScore': 'PS评分', 'examMethod': '影像学检查','smokingHis': '吸烟史',
                 'drinkingHis': '饮酒史', 'firVisDate': '初诊日期', 'bioMet': '活检方式',
                 'speSite': '标本部位', 'patReDate': '病理报告日期', 'patNum': '病理号',
                 'patDia': '病理诊断', 'cStage-T': 'c分期T', 'cStage-N': 'c分期N',
                 'cStage-M': 'c分期M', 'cliStage': '临床分期', 'pStage-T': 'p分期T',
                 'pStage-N': 'p分期N', 'pStage-M': 'p分期M', 'patStage': '病理分期',
                 'traSite': '转移部位', 'surDate': '手术时间', 'surSco': '手术范围',
                 'isRepBio': '术后病理', 'specNum': '病理号', 'posAdjChem': '术后辅助化疗',
                 'surgery_begDate': '辅助治疗开始时间', 'surgery_endDate': '辅助治疗结束时间', 'sidReaName': '副反应',
                 'positiveGene': '阳性基因', 'PDL1': 'PD-L1表达水平', 'TMB': 'TMB',
                 'radSite': '放疗部位', 'radDose': '放疗剂量', 'splTim': '分割次数',
                 'radio_begDate': '放疗开始时间', 'radio_endDate': '放疗结束时间',
                 'beEffEva': '疗效评价', 'livSta': '生存状态', 'dieDate': '死亡时间',
                 'date': '最后一次随访日期'
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

    def __init__(self, pids, tables, columns):
        self.buffer = []
        self.headers = []
        self.pids = pids
        self.tables = tables
        self.columns = columns
        for x in columns:
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
        self.init_buffer()

    def init_buffer(self):
        for obj_class_name in self.tables:
            if obj_class_name.__name__ == 'Patient':
                obj_array = obj_class_name.query.filter(obj_class_name.id.in_(self.pids),
                                                        obj_class_name.is_delete == 0).all()
            else:
                obj_array = obj_class_name.query.filter(obj_class_name.pid.in_(self.pids),
                                                        obj_class_name.is_delete == 0).all()
            self.buffer.append(self.classify_by_pid(obj_array))

    def work(self):
        wb = Workbook()
        ws = wb.active
        ws.title = '导出样本数据'
        ws.append(self.headers)

        for pid in self.pids:
            row = []
            i = 0
            for dic in self.buffer:
                for strib in self.columns[i]:
                    try:
                        if strib == 'gender':
                            temp = self.filter_none(dic[pid], strib)
                            row.append(self.gender_map.get(temp))
                        elif strib == 'age':
                            temp = getattr(dic[pid], 'idNumber')
                            age = get_age_by_birth(get_birth_date_by_id_card(temp))
                            age = age if age else '/'
                            row.append(age)
                        elif strib == 'drinkingHis':
                            temp = self.format_drink_history(dic[pid])
                            row.append(temp)
                        elif strib == 'smokingHis':
                            temp = self.format_smoke_history(dic[pid])
                            row.append(temp)
                        elif strib == 'bioMet' or strib == 'traSite':
                            temp = self.format_radio_data(dic[pid], strib)
                            row.append(temp)
                        elif strib == 'patDia':
                            temp = self.format_patDia(dic[pid])
                            row.append(temp)
                        elif strib == 'cStage' or strib == 'pStage':
                            stage_array = self.format_stage(dic[pid], strib)
                            row.extend(stage_array)
                        else:
                            temp = self.filter_none(dic[pid], strib)
                            row.append(temp)
                    except KeyError:
                        row.append("/")
                        print("KeyError没有找到该键！")
                i += 1
            ws.append(row)

        wb.save('test.xlsx')
        content = save_virtual_workbook(wb)
        resp = make_response(content)
        resp.headers["Content-Disposition"] = 'attachment; filename=samples.xlsx'
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp

    def classify_by_pid(self, items):
        data = {}
        for item in items:
            if getattr(item, 'pid', None):
                data[item.pid] = item
            else:
                data[item.id] = item
        return data

    def filter_none(self,data,item=None):
        if data is None:
            return '/'
        if item:
            val = getattr(data,item)
        else:
            val = data
        return val if val is not None else '/'

    def format_smoke_history(self,object):
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

    def format_drink_history(self,object):
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

    def format_radio_data(self,object,item):
        if object is None:
            return '/'
        data = getattr(object,item)
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
        data = getattr(object,item)
        if data is None or data == "":
            return value
        ret = data.split(',')
        for i in range(0, 3):
            value[i] = self.filter_none(ret[i])
        return value
