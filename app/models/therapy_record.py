from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base, db

# 治疗记录及疗效评估表
from app.models.cycle import Immunohis, MoleDetec, Signs, SideEffect
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams


class PatDia:
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


class TreRec(Base, PatDia):
    __tablename__ = 'treRec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='1-n，表示对应第x条治疗记录')
    trement = Column(String(255), comment='几线治疗（手术、放疗、其他、1-5）(one,two,three,four,five,surgery,radiotherapy,other)')
    date = Column(DateTime, comment='结束日期')
    beEffEvaDate = Column(Date, comment='最佳疗效评估日期')
    beEffEva = Column(String(255), comment='最佳疗效评估')
    proDate = Column(Date, comment='进展日期')
    proDes = Column(String(2048), comment='进展描述')  # text
    PFS_DFS = Column(String(2048), comment='PFS/DFS')

    # 和导出功能有关
    export_header_map = {'trement': '几线治疗', 'beEffEvaDate': '最佳疗效评估日期', 'beEffEva': '最佳疗效评估',
                         'proDate': '进展日期', 'proDes': '进展描述', 'PFS_DFS': 'PFS/DFS',
                         'isRepBio': '是否重复活检', 'bioMet': '活检方式', 'matPart': '取材部位', 'specNum': '标本库流水号',
                         'patDia': '病理诊断'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treNum):
        row = []
        if buffer.get('TreRec').get(pid) is None or buffer.get('TreRec').get(pid).get(treNum) is None:
            for k in range(0, TreRec.header_num):
                row.append('/')
            return row
        obj = buffer.get('TreRec').get(pid).get(treNum)

        if obj.trement == 'surgery':
            if buffer.get('Surgery').get(pid) is None or buffer.get('Surgery').get(pid).get(treNum) is None:
                obj2 = None
            else:
                obj2 = buffer.get('Surgery').get(pid).get(treNum)
        elif obj.trement == 'radiotherapy':
            if buffer.get('Radiotherapy').get(pid) is None or buffer.get('Radiotherapy').get(pid).get(treNum) is None:
                obj2 = None
            else:
                obj2 = buffer.get('Radiotherapy').get(pid).get(treNum)
        elif obj.trement in ['one', 'two', 'three', 'four', 'five']:
            if buffer.get('OneToFive').get(pid) is None or buffer.get('OneToFive').get(pid).get(treNum) is None:
                obj2 = None
            else:
                obj2 = buffer.get('OneToFive').get(pid).get(treNum)
        else:
            obj2 = None

        for column in columns:
            if column == 'trement':
                trement_map = {'one': '1线', 'two': '2线', 'three': '3线', 'four': '4线',
                               'five': '5线', 'surgery': '手术', 'radiotherapy': '放疗', 'other': '其他', '/': '/'}
                value = self.filter_none(obj, column)
                value = trement_map.get(value)
                row.append(value)
            elif column == 'isRepBio':
                value = self.filter_none(self.change_bool_to_yes_or_no(getattr(obj2, column))) if obj2 else '/'
                row.append(value)
            elif column == 'matPart' or column == 'specNum':
                value_isRepBio = getattr(obj2, 'isRepBio') if obj2 else None
                value = self.filter_none(obj2, column) if value_isRepBio else '/'
                row.append(value)
            elif column == 'bioMet':
                value_isRepBio = getattr(obj2, 'isRepBio') if obj2 else None
                value = self.format_radio_data(obj2, column) if value_isRepBio else '/'
                row.append(value)
            elif column == 'patDia':
                value_isRepBio = getattr(obj2, 'isRepBio') if obj2 else None
                value = self.format_patDia(obj2) if value_isRepBio else '/'
                row.append(value)
            else:
                value = self.filter_none(obj, column)
                row.append(value)

        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = []
        for column in columns:
            header.append(self.export_header_map.get(column))
        TreRec.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'treNum', 'trement', 'date', 'beEffEvaDate', 'beEffEva', 'proDate', 'proDes', 'PFS_DFS']

    def get_parent(self):
        data = {
            'id': self.id,
            'trement': self.trement
        }
        return data

    def compute_FPS_DFS(self):
        date1 = None
        if self.trement == 'surgery':
            surgery = Surgery.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            if surgery:
                date1 = surgery.surDate
        elif self.trement in ["one", "two", "three", "four", "five", 'other']:
            trePlan = DetailTrePlan.query.filter_by(pid=self.pid, treNum=self.treNum).order_by(
                DetailTrePlan.begDate).first()
            if trePlan:
                date1 = trePlan.begDate
        date2 = self.proDate
        if date1 and date2:
            with db.auto_commit():
                months = (date2 - date1).days / 30
                time = str(round(months, 1)) + "月"
                self.PFS_DFS = time

    def get_child(self):
        trement = self.trement
        if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
            child = OneToFive.query.filter_by(pid=self.pid, treNum=self.treNum).first()
        elif trement == 'surgery':
            child = Surgery.query.filter_by(pid=self.pid, treNum=self.treNum).first()
        elif trement == 'radiotherapy':
            child = Radiotherapy.query.filter_by(pid=self.pid, treNum=self.treNum).first()
        else:
            child = {}
        return child if child else {}

    def delete(self):
        with db.auto_commit():
            self.is_delete = 1
            self.delete_in_cycle(OneToFive)
            self.delete_in_cycle(DetailTrePlan)
            self.delete_in_cycle(Surgery)
            self.delete_in_cycle(Radiotherapy)

            # 删除实验室检查
            self.delete_in_cycle(BloodRoutine)
            self.delete_in_cycle(BloodBio)
            self.delete_in_cycle(Thyroid)
            self.delete_in_cycle(Coagulation)
            self.delete_in_cycle(MyocardialEnzyme)
            self.delete_in_cycle(Cytokines)
            self.delete_in_cycle(LymSubsets)
            self.delete_in_cycle(UrineRoutine)
            self.delete_in_cycle(TumorMarker)

            # 删除其他检查
            self.delete_in_cycle(Lung)
            self.delete_in_cycle(OtherExams)
            self.delete_in_cycle(ImageExams)

            # 删除免疫组化，分子检测，症状体征，副反应
            self.delete_in_cycle(Immunohis)
            self.delete_in_cycle(MoleDetec)
            self.delete_in_cycle(Signs)
            self.delete_in_cycle(SideEffect)

    def delete_in_cycle(self, table):

        records = table.query.filter_by(pid=self.pid, treNum=self.treNum).all()
        with db.auto_commit():
            for record in records:
                record.delete()


# 1-5线及其他表
class OneToFive(Base, PatDia):
    __tablename__ = 'oneToFive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    isTre = Column(Integer, comment='是否加入临床治疗')
    clinTri = Column(String(40), comment='临床实验名称')  # 长度
    treSolu = Column(String(100),
                     comment='治疗方案,多个以逗号分隔(Chemotherapy,TargetedTherapy,ImmunityTherapy,AntivascularTherapy,Other)')  # 长度
    spePlan = Column(String(60), comment='具体方案')
    begDate = Column(Date, comment='开始日期')
    endDate = Column(Date, comment='结束日期')
    isRepBio = Column(Boolean, comment='是否重复活检')
    bioMet = Column(JSON, comment='活检方式')  # 长度
    _bioMet = Column(String(40), comment='活检方式')  # 长度
    matPart = Column(String(255), comment='取材部位')  # 长度
    specNum = Column(String(255), comment='标本库流水号')  # 类型 改为字符串
    patDia = Column(JSON, comment='病理诊断结果')
    patDiaRes = Column(Text(10000), comment='病理诊断结果')
    patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    # patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    note = Column(String(2048), comment='备注')

    # 和导出功能有关
    chemo_detail_num = 0
    targeted_detail_num = 0
    immunity_detail_num = 0
    antivascular_detail_num = 0
    export_header_map = {'isTre': '是否加入临床治疗', 'clinTri': '临床实验名称', 'treSolu': '治疗方案',
                         'note': '备注', 'begDate': '开始日期', 'endDate': '结束日期',
                         'treatName': '治疗名称', 'currPeriod': '周期', 'treSche': '药物方案',
                         'drugs': '药物', 'detailBegDate': '给药/治疗开始日期', 'detailEndDate': '给药/治疗结束日期', 'detailNote': '备注'}
    detail_header = ['treatName', 'currPeriod', 'treSche', 'drugs', 'detailBegDate', 'detailEndDate', 'detailNote']

    def keys(self):
        return ['id', 'pid', 'treNum', 'isTre', 'clinTri', 'treSolu', 'spePlan', 'begDate',
                'endDate', 'isRepBio', 'bioMet', 'matPart', 'specNum', 'patDiaRes', 'patDiaOthers', 'note', 'patDia',
                '_bioMet']

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treNum):
        isTre_map = {0: '否', 1: '是', -1: '不详', "/": "/"}
        chemo_detail_trePlan_array = None
        targeted_detail_trePlan_array = None
        immunity_detail_trePlan_array = None
        antivascular_detail_trePlan_array = None
        row = []
        if (buffer.get('OneToFive').get(pid) is None or buffer.get('OneToFive').get(pid).get(treNum) is None
                or buffer.get('TreRec').get(pid) is None or buffer.get('TreRec').get(pid).get(treNum) is None
                or not (buffer.get('TreRec').get(pid).get(treNum).trement in ['one', 'two', 'three', 'four', 'five'])):
            for k in range(0, OneToFive.header_num):
                row.append('/')
            return row
        obj = buffer.get('OneToFive').get(pid).get(treNum)

        detail_columns = []
        for k in range(0, len(columns)):
            if columns[k] in self.detail_header:
                detail_columns.append(columns[k])

        if buffer.get('DetailTrePlan').get(pid) is None or buffer.get('DetailTrePlan').get(pid).get(treNum) is None:
            detail_trePlan_array = None
        else:
            detail_trePlan_array = buffer.get('DetailTrePlan').get(pid).get(treNum)
        detail_flag = False #标志是否已经处理了详细治疗方案的字段

        for column in columns:
            if column == 'isTre':
                value = self.filter_none(obj, column)
                value = isTre_map.get(value)
                row.append(value)
            elif column == 'clinTri':
                value_isTre = self.filter_none(obj, 'isTre')
                value = self.filter_none(obj, column) if value_isTre == 1 else '/'
                row.append(value)
            elif column == 'treSolu':
                value = ''
                treSolu_value = self.filter_none(obj, column)
                if 'Chemotherapy' in treSolu_value:
                    value += '化疗 '
                if 'TargetedTherapy' in treSolu_value:
                    value += '靶向治疗 '
                if 'ImmunityTherapy' in treSolu_value:
                    value += '免疫治疗 '
                if 'AntivascularTherapy' in treSolu_value:
                    value += '抗血管治疗 '
                if 'Other' in treSolu_value:
                    value += '其他 '
                row.append(value)
            elif column in detail_columns and not detail_flag:
                detail_flag = True
                treSolu_value = self.filter_none(obj, 'treSolu')
                if not detail_trePlan_array:
                    for k in range(0, OneToFive.chemo_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
                    for k in range(0, OneToFive.targeted_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
                    for k in range(0, OneToFive.immunity_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
                    for k in range(0, OneToFive.antivascular_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
                else:
                    chemo_detail_num = 0
                    targeted_detail_num = 0
                    immunity_detail_num = 0
                    antivascular_detail_num = 0

                    if 'Chemotherapy' in treSolu_value and detail_trePlan_array.get('Chemotherapy'):
                        chemo_detail_trePlan_array = detail_trePlan_array['Chemotherapy']
                        chemo_detail_num = len(chemo_detail_trePlan_array)
                        for detail_trePlan in chemo_detail_trePlan_array:
                            for detail_column in detail_columns:
                                if detail_column == 'drugs':
                                    value_drugs = self.filter_none(detail_trePlan, 'drugs')
                                    drugs = ''
                                    if type(value_drugs) == dict:
                                        for key, value in value_drugs.items():
                                            drugs += key + ':'
                                            if 'drugDosa' in value.keys():
                                                drugs += str(self.filter_none(value['drugDosa']))
                                            if 'unit' in value.keys():
                                                drugs += self.filter_none(value['unit'])
                                            drugs += '  '
                                    elif type(value_drugs) == list:
                                        for each in value_drugs:
                                            if 'name' in each.keys():
                                                drugs += self.filter_none(each['name']) + ':'
                                            if 'dose' in each.keys():
                                                drugs += self.filter_none(each['dose'])
                                            drugs += '  '
                                    else:
                                        drugs = str(value_drugs)
                                    row.append(drugs)
                                elif detail_column == 'detailBegDate':
                                    row.append(self.filter_none(detail_trePlan, 'begDate'))
                                elif detail_column == 'detailEndDate':
                                    row.append(self.filter_none(detail_trePlan, 'endDate'))
                                elif detail_column == 'detailNote':
                                    row.append(self.filter_none(detail_trePlan, 'note'))
                                else:
                                    row.append(self.filter_none(detail_trePlan, detail_column))

                    for k in range(0, OneToFive.chemo_detail_num - chemo_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')

                    if 'TargetedTherapy' in treSolu_value and detail_trePlan_array.get('TargetedTherapy'):
                        targeted_detail_trePlan_array = detail_trePlan_array['TargetedTherapy']
                        targeted_detail_num = len(targeted_detail_trePlan_array)
                        for detail_trePlan in targeted_detail_trePlan_array:
                            for detail_column in detail_columns:
                                if detail_column == 'drugs':
                                    value_drugs = self.filter_none(detail_trePlan, 'drugs')
                                    drugs = ''
                                    if type(value_drugs) == dict:
                                        for key, value in value_drugs.items():
                                            drugs += key + ':'
                                            if 'drugDosa' in value.keys():
                                                drugs += str(self.filter_none(value['drugDosa']))
                                            if 'unit' in value.keys():
                                                drugs += self.filter_none(value['unit'])
                                            drugs += '  '
                                    elif type(value_drugs) == list:
                                        for each in value_drugs:
                                            if 'name' in each.keys():
                                                drugs += self.filter_none(each['name']) + ':'
                                            if 'dose' in each.keys():
                                                drugs += self.filter_none(each['dose'])
                                            drugs += '  '
                                    else:
                                        drugs = str(value_drugs)
                                    row.append(drugs)
                                elif detail_column == 'detailBegDate':
                                    row.append(self.filter_none(detail_trePlan, 'begDate'))
                                elif detail_column == 'detailEndDate':
                                    row.append(self.filter_none(detail_trePlan, 'endDate'))
                                elif detail_column == 'detailNote':
                                    row.append(self.filter_none(detail_trePlan, 'note'))
                                else:
                                    row.append(self.filter_none(detail_trePlan, detail_column))

                    for k in range(0, OneToFive.targeted_detail_num - targeted_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')

                    if 'ImmunityTherapy' in treSolu_value and detail_trePlan_array.get('ImmunityTherapy'):
                        immunity_detail_trePlan_array = detail_trePlan_array['ImmunityTherapy']
                        immunity_detail_num = len(immunity_detail_trePlan_array)
                        for detail_trePlan in immunity_detail_trePlan_array:
                            for detail_column in detail_columns:
                                if detail_column == 'drugs':
                                    value_drugs = self.filter_none(detail_trePlan, 'drugs')
                                    drugs = ''
                                    if type(value_drugs) == dict:
                                        for key, value in value_drugs.items():
                                            drugs += key + ':'
                                            if 'drugDosa' in value.keys():
                                                drugs += str(self.filter_none(value['drugDosa']))
                                            if 'unit' in value.keys():
                                                drugs += self.filter_none(value['unit'])
                                            drugs += '  '
                                    elif type(value_drugs) == list:
                                        for each in value_drugs:
                                            if 'name' in each.keys():
                                                drugs += self.filter_none(each['name']) + ':'
                                            if 'dose' in each.keys():
                                                drugs += self.filter_none(each['dose'])
                                            drugs += '  '
                                    else:
                                        drugs = str(value_drugs)
                                    row.append(drugs)
                                elif detail_column == 'detailBegDate':
                                    row.append(self.filter_none(detail_trePlan, 'begDate'))
                                elif detail_column == 'detailEndDate':
                                    row.append(self.filter_none(detail_trePlan, 'endDate'))
                                elif detail_column == 'detailNote':
                                    row.append(self.filter_none(detail_trePlan, 'note'))
                                else:
                                    row.append(self.filter_none(detail_trePlan, detail_column))

                    for k in range(0, OneToFive.immunity_detail_num - immunity_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')

                    if 'AntivascularTherapy' in treSolu_value and detail_trePlan_array.get('AntivascularTherapy'):
                        antivascular_detail_trePlan_array = detail_trePlan_array['AntivascularTherapy']
                        antivascular_detail_num = len(antivascular_detail_trePlan_array)
                        for detail_trePlan in antivascular_detail_trePlan_array:
                            for detail_column in detail_columns:
                                if detail_column == 'drugs':
                                    value_drugs = self.filter_none(detail_trePlan, 'drugs')
                                    drugs = ''
                                    if type(value_drugs) == dict:
                                        for key, value in value_drugs.items():
                                            drugs += key + ':'
                                            if 'drugDosa' in value.keys():
                                                drugs += str(self.filter_none(value['drugDosa']))
                                            if 'unit' in value.keys():
                                                drugs += self.filter_none(value['unit'])
                                            drugs += '  '
                                    elif type(value_drugs) == list:
                                        for each in value_drugs:
                                            if 'name' in each.keys():
                                                drugs += self.filter_none(each['name']) + ':'
                                            if 'dose' in each.keys():
                                                drugs += self.filter_none(each['dose'])
                                            drugs += '  '
                                    else:
                                        drugs = str(value_drugs)
                                    row.append(drugs)
                                elif detail_column == 'detailBegDate':
                                    row.append(self.filter_none(detail_trePlan, 'begDate'))
                                elif detail_column == 'detailEndDate':
                                    row.append(self.filter_none(detail_trePlan, 'endDate'))
                                elif detail_column == 'detailNote':
                                    row.append(self.filter_none(detail_trePlan, 'note'))
                                else:
                                    row.append(self.filter_none(detail_trePlan, detail_column))

                    for k in range(0, OneToFive.antivascular_detail_num - antivascular_detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')

            elif column == 'note':
                value_treSolu = self.filter_none(obj, 'treSolu')
                if 'Other' in value_treSolu:
                    value = self.filter_none(obj, column)
                else:
                    value = '/'
                row.append(value)
            elif not (column in detail_columns):
                value = self.filter_none(obj, column)
                row.append(value)

        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = []
        # 求最多有多少条
        max_chemo_detail_num = 0
        max_targeted_detail_num = 0
        max_immunity_detail_num = 0
        max_antivascular_detail_num = 0

        detail_columns = []
        for k in range(0, len(columns)):
            if columns[k] in self.detail_header:
                detail_columns.append(columns[k])

        for value1 in buffer.get('DetailTrePlan').values():
            for value2 in value1.values():
                if value2:
                    chemo_detail_num = len(value2.get('Chemotherapy')) if value2.get('Chemotherapy') else 0
                    targeted_detail_num = len(value2.get('TargetedTherapy')) if value2.get('TargetedTherapy') else 0
                    immunity_detail_num = len(value2.get('ImmunityTherapy')) if value2.get('ImmunityTherapy') else 0
                    antivascular_detail_num = len(value2.get('AntivascularTherapy')) if value2.get(
                        'AntivascularTherapy') else 0

                    if chemo_detail_num > max_chemo_detail_num:
                        max_chemo_detail_num = chemo_detail_num
                    if targeted_detail_num > max_targeted_detail_num:
                        max_targeted_detail_num = targeted_detail_num
                    if immunity_detail_num > max_immunity_detail_num:
                        max_immunity_detail_num = immunity_detail_num
                    if antivascular_detail_num > max_antivascular_detail_num:
                        max_antivascular_detail_num = antivascular_detail_num

        detail_flag = False #标志是否已经处理详细治疗方案字段
        for column in columns:
            if column == 'treSolu':
                header.append(self.export_header_map.get(column))
            elif column in detail_columns and not detail_flag:
                detail_flag = True
                for k in range(1, max_chemo_detail_num + 1):
                    for detail_column in detail_columns:
                        header.append('化疗:' + self.export_header_map.get(detail_column) + str(k))
                for k in range(1, max_targeted_detail_num + 1):
                    for detail_column in detail_columns:
                        header.append('靶向治疗:' + self.export_header_map.get(detail_column) + str(k))
                for k in range(1, max_immunity_detail_num + 1):
                    for detail_column in detail_columns:
                        header.append('免疫治疗:' + self.export_header_map.get(detail_column) + str(k))
                for k in range(1, max_antivascular_detail_num + 1):
                    for detail_column in detail_columns:
                        header.append('抗血管治疗:' + self.export_header_map.get(detail_column) + str(k))
            elif not (column in detail_columns):
                header.append(self.export_header_map.get(column))

        OneToFive.chemo_detail_num = max_chemo_detail_num
        OneToFive.targeted_detail_num = max_targeted_detail_num
        OneToFive.immunity_detail_num = max_immunity_detail_num
        OneToFive.antivascular_detail_num = max_antivascular_detail_num
        OneToFive.header_num = len(header)
        return header


# 详细治疗方案
class DetailTrePlan(Base):
    __tablename__ = 'DetailTrePlan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    treSolu = Column(String(255), comment='治疗方案,Chemotherapy/TargetedTherapy/ImmunityTherapy/AntivascularTherapy/Other')
    treSche = Column(String(255), comment='药物方案')  # 长度
    currPeriod = Column(Integer, comment='当前周期')
    treatName = Column(String(255), comment='治疗名称')  # 长度
    begDate = Column(Date, comment='开始时间')
    endDate = Column(Date, comment='结束时间')
    drugs = Column(JSON, comment='药物使用情况, {drugName:{drugDosa: ,duration: },...}')
    note = Column(String(2048), comment='药物使用备注')  # 长度

    def keys(self):
        return ['id', 'treSolu', 'treSche', 'currPeriod', 'treatName', 'begDate', 'endDate', 'drugs', 'note']


# 手术表
class Surgery(Base, PatDia):
    __tablename__ = 'surgery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    surSco = Column(JSON, comment='手术范围')
    _surSco = Column(JSON, comment='手术范围')
    lymDis = Column(JSON, comment='淋巴清扫范围')
    _lymDis = Column(JSON, comment='淋巴清扫范围')
    cleGro = Column(String(40), comment='清扫组数')
    surDate = Column(Date, comment='手术日期')
    posAdjChem = Column(Boolean, comment='术后辅助化疗')
    isPro = Column(Boolean, comment='是否进展')
    proDate = Column(Date, comment='进展日期')
    proDes = Column(String(2048), comment='进展描述')
    isRepBio = Column(Boolean, comment='是否重复活检')
    # bioMet = Column(JSON, comment='活检方式')  # 长度
    bioMet = Column(JSON, comment='活检方式')  # 长度
    matPart = Column(String(255), comment='取材部位')
    specNum = Column(String(255), comment='标本库流水号')
    patDia = Column(JSON, comment='病理诊断结果')

    # 和导出功能有关
    detail_header_num = 0
    export_header_map = {'surSco': '手术范围', 'lymDis': '淋巴清扫范围',
                         'cleGro': '清扫组数', 'surDate': '手术日期', 'posAdjChem': '术后辅助化疗',
                         'treatName': '治疗名称', 'currPeriod': '周期', 'treSche': '药物方案',
                         'drugs': '药物', 'detailBegDate': '给药/治疗开始日期', 'detailEndDate': '给药/治疗结束日期', 'detailNote': '备注'}
    detail_header = ['treatName', 'currPeriod', 'treSche', 'drugs', 'detailBegDate', 'detailEndDate',
                     'detailNote']  # 和导出功能有关

    def get_export_row(self, columns, buffer, pid, treNum):
        row = []
        if (buffer.get('Surgery').get(pid) is None or buffer.get('Surgery').get(pid).get(treNum) is None
                or buffer.get('TreRec').get(pid) is None or buffer.get('TreRec').get(pid).get(treNum) is None
                or buffer.get('TreRec').get(pid).get(treNum).trement != 'surgery'):
            for k in range(0, Surgery.header_num):
                row.append('/')
            return row
        obj = buffer.get('Surgery').get(pid).get(treNum)

        detail_columns = []
        for k in range(0, len(columns)):
            if columns[k] in self.detail_header:
                detail_columns.append(columns[k])

        if buffer.get('DetailTrePlan').get(pid) is None or buffer.get('DetailTrePlan').get(pid).get(treNum) is None:
            detail_trePlan_array = None
        else:
            detail_trePlan_array = buffer.get('DetailTrePlan').get(pid).get(treNum)

        detail_flag = False # 标志是否已经处理详细治疗方案字段
        for column in columns:
            if column == 'surSco' or column == 'lymDis':
                value = self.format_radio_data(obj, column)
                row.append(value)
            elif column == 'posAdjChem':
                value = self.filter_none(self.change_bool_to_yes_or_no(getattr(obj, column)))
                row.append(value)
            elif column in detail_columns and not detail_flag:
                detail_flag = True
                posAdjChem_value = self.filter_none(self.change_bool_to_yes_or_no(getattr(obj, 'posAdjChem')))
                if posAdjChem_value != '是' or not detail_trePlan_array or not detail_trePlan_array.get('Chemotherapy'):
                    for k in range(0, Surgery.detail_header_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
                else:
                    surgery_detail_trePlan_array = detail_trePlan_array.get('Chemotherapy')
                    detail_num = len(surgery_detail_trePlan_array)
                    for detail_trePlan in surgery_detail_trePlan_array:
                        for detail_column in detail_columns:
                            if detail_column == 'drugs':
                                value_drugs = self.filter_none(detail_trePlan, detail_column)
                                drugs = ''
                                if type(value_drugs) == dict:
                                    for key, value in value_drugs.items():
                                        drugs += key + ':'
                                        if 'drugDosa' in value.keys():
                                            drugs += self.filter_none(str(value['drugDosa']))
                                        if 'unit' in value.keys():
                                            drugs += self.filter_none(str(value['drugDosa']))
                                        drugs += '  '
                                elif type(value_drugs) == list:
                                    for each in value_drugs:
                                        if 'name' in each.keys():
                                            drugs += self.filter_none(each['name']) + ':'
                                        if 'dose' in each.keys():
                                            drugs += self.filter_none(each['name'])
                                        drugs += '  '
                                else:
                                    drugs = str(value_drugs)
                                row.append(drugs)
                            elif detail_column == 'detailBegDate':
                                row.append(self.filter_none(detail_trePlan, 'begDate'))
                            elif detail_column == 'detailEndDate':
                                row.append(self.filter_none(detail_trePlan, 'endDate'))
                            elif detail_column == 'detailNote':
                                row.append(self.filter_none(detail_trePlan, 'note'))
                            else:
                                row.append(self.filter_none(detail_trePlan, detail_column))

                    for k in range(0, Surgery.detail_header_num - detail_num):
                        for i in range(0, len(detail_columns)):
                            row.append('/')
            elif not (column in detail_columns):
                value = self.filter_none(obj, column)
                row.append(value)

        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = []

        detail_columns = []
        for k in range(0, len(columns)):
            if columns[k] in self.detail_header:
                detail_columns.append(columns[k])

        # 求最多有多少条
        max_num = 0
        for value1 in buffer.get('DetailTrePlan').values():
            for value2 in value1.values():
                if value2 and value2.get('Chemotherapy'):
                    num = len(value2.get('Chemotherapy'))

                    if num > max_num:
                        max_num = num

        if max_num > 1:
            header_num = max_num
        else:
            header_num = 1

        detail_flag = False  # 标志是否已经处理详细治疗方案字段
        for column in columns:
            if column == 'posAdjChem':
                header.append(self.export_header_map.get(column))
            elif column in detail_columns and not detail_flag:
                detail_flag = True
                for k in range(1, header_num + 1):
                    for detail_column in detail_columns:
                        header.append('术后辅助化疗:' + self.export_header_map.get(detail_column) + str(k))
            elif not (column in detail_columns):
                header.append(self.export_header_map.get(column))

        Surgery.detail_header_num = header_num
        Surgery.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'surSco', 'lymDis', 'cleGro', 'surDate', 'posAdjChem', 'isPro', 'proDate',
                'proDes',
                'isRepBio', 'bioMet', 'matPart', 'specNum', 'patDia',
                '_surSco', '_lymDis']


# 放疗表
class Radiotherapy(Base):
    __tablename__ = 'radiotherapy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    begDate = Column(Date, comment='开始日期')
    endDate = Column(Date, comment='结束日期')

    _radSite = Column(JSON, comment='放疗部位')
    radSite = Column(JSON, comment='放疗部位')

    radDose = Column(Float, comment='放射剂量')
    dosUnit = Column(Boolean, comment='剂量单位,0: Gy, 1:cGy')
    splTim = Column(Integer, comment='分割次数')
    method = Column(String(255), comment='分割次数单位')
    isRepBio = Column(Boolean, comment='是否重复活检')
    # bioMet = Column(JSON, comment='活检方式')  # 长度
    bioMet = Column(JSON, comment='活检方式')  # 长度
    matPart = Column(String(255), comment='取材部位')
    specNum = Column(String(255), comment='标本库流水号')
    patDia = Column(JSON, comment='病理诊断结果')

    # 和导出功能有关
    export_header_map = {'begDate': '开始日期', 'endDate': '结束日期', 'radSite': '放疗部位',
                         'radDose': '放疗剂量', 'splTim': '分割次数'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treNum):
        radosUnit_map = {0: 'Gy', 1: 'cGy', "/": "/"}

        row = []
        if (buffer.get('Radiotherapy').get(pid) is None or buffer.get('Radiotherapy').get(pid).get(treNum) is None
                or buffer.get('TreRec').get(pid) is None or buffer.get('TreRec').get(pid).get(treNum) is None
                or buffer.get('TreRec').get(pid).get(treNum).trement != 'radiotherapy'):
            for k in range(0, Radiotherapy.header_num):
                row.append('/')
            return row
        obj = buffer.get('Radiotherapy').get(pid).get(treNum)
        for column in columns:
            if column == 'radSite':
                value = self.format_radio_data(obj, column)
                row.append(value)
            elif column == 'radDose':
                value_radDose = self.filter_none(obj, column)
                value_dosUnit = radosUnit_map.get(self.filter_none(obj, 'dosUnit'))
                value = str(value_radDose) + value_dosUnit if value_radDose != '/' else '/'
                row.append(value)
            elif column == 'splTim':
                value_splTim = self.filter_none(obj, column)
                value_method = self.filter_none(obj, 'method')
                value = str(value_splTim) + value_method if value_splTim != '/' else '/'
                row.append(value)

            else:
                value = self.filter_none(obj, column)
                row.append(value)

        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = []
        for column in columns:
            header.append(self.export_header_map.get(column))
        Radiotherapy.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'begDate', 'endDate', 'radSite', 'radDose', 'dosUnit', 'splTim', 'method',
                '_radSite',
                'isRepBio', 'bioMet', 'matPart', 'specNum', 'patDia']
