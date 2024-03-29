from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime, JSON
from app.models.base import Base, ModificationAndDoubt
import numpy as np


# 病人免疫组化信息表
class Immunohis(Base, ModificationAndDoubt):
    __tablename__ = 'immunohis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    detectTime = Column(Date, comment='检测时间')
    patNum = Column(String(255), comment='病理号')
    ALKD5F3 = Column(Integer, comment='ALKD5F3 0:-,1:±,2:+,3:++,4:+++')
    ALKD5F3N = Column(Integer, comment='ALKD5F3-N')
    CAIX = Column(Integer, comment='CAIX')
    CAM52 = Column(Integer, comment='CAM5.2')
    CD10 = Column(Integer, comment='CD10')
    CD34 = Column(Integer, comment='CD34')
    CD56 = Column(Integer, comment='CD56')
    CD117 = Column(Integer, comment='CD117')
    CDX2 = Column(Integer, comment='CDX-2')
    CD516 = Column(Integer, comment='CD516')
    CEA = Column(Integer, comment='CEA')
    CgA = Column(Integer, comment='CgA')
    CK = Column(Integer, comment='CK')
    CK56 = Column(Integer, comment='CK5/6')
    CK7 = Column(Integer, comment='CK7')
    CK818 = Column(Integer, comment='CK8/18')
    CK19 = Column(Integer, comment='CK19')
    CK20 = Column(Integer, comment='CK20')
    Cyn = Column(Integer, comment='Cyn')
    DLL3 = Column(Integer, comment='DLL3')
    EMA = Column(Integer, comment='EMA')
    ERCC1 = Column(Integer, comment='ERCC-1')
    LCA = Column(Integer, comment='LCA')
    MCM2 = Column(Integer, comment='MCM2')
    NapsinA = Column(Integer, comment='Napsin A')
    P16 = Column(Integer, comment='P16')
    P40 = Column(Integer, comment='P40')
    p53 = Column(Integer, comment='p53')
    P63 = Column(Integer, comment='P63')
    PAX2 = Column(Integer, comment='PAX-2')
    PAX8 = Column(Integer, comment='PAX-8')
    PCK = Column(Integer, comment='PCK')
    PDL1 = Column(Integer, comment='PD-L1')
    RRM1 = Column(Integer, comment='RRM-1')
    SATB2 = Column(Integer, comment='SATB2')
    Syn = Column(Integer, comment='Syn')
    TTF1 = Column(Integer, comment='TTF1')
    VEGFC = Column(Integer, comment='VEGF-C')
    Villin = Column(Integer, comment='Villin')
    Villinco = Column(Integer, comment='Villin')
    Ki67 = Column(Float, comment='Ki67')
    other = Column(String(2048), comment='其他')  # 长度
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'ALKD5F3': 'ALKD5F3', 'ALKD5F3N': 'ALKD5F3N', 'CAIX': 'CAIX', 'CAM52': 'CAM52', 'CD10': 'CD10',
                         'CD34': 'CD34', 'CD56': 'CD56', 'CD117': 'CD117', 'CDX2': 'CDX2', 'CEA': 'CEA', 'CgA': 'CgA',
                         'CK': 'CK', 'CK56': 'CK56', 'CK7': 'CK7', 'CK818': 'CK818', 'CK19': 'CK19', 'CK20': 'CK20',
                         'Cyn': 'Cyn', 'DLL3': 'DLL3', 'EMA': 'EMA', 'ERCC1': 'ERCC1', 'LCA': 'LCA', 'MCM2': 'MCM2',
                         'NapsinA': 'NapsinA', 'P16': 'P16', 'P40': 'P40', 'p53': 'p53', 'P63': 'P63', 'PAX2': 'PAX2',
                         'PAX8': 'PAX8', 'PCK': 'PCK', 'PDL1': 'PDL1', 'RRM1': 'RRM1', 'SATB2': 'SATB2', 'Syn': 'Syn',
                         'TTF1': 'TTF1', 'VEGFC': 'VEGFC', 'Villin': 'Villin', 'Villinco': 'Villinco', 'CD516': 'CD516',
                         'other': '其他', 'Ki67': 'Ki67', 'detectTime': '免疫组化检测时间', 'patNum': '病理号'}

    def keys(self):
        return ['id', 'pid', 'treNum', 'ALKD5F3', 'ALKD5F3N', 'CAIX', 'CAM52', 'CD10', 'CD34', 'CD56',
                'CD117', 'CDX2', 'CEA', 'CgA', 'CK', 'CK56', 'CK7', 'CK818', 'CK19', 'CK20', 'Cyn', 'DLL3', 'EMA',
                'ERCC1', 'LCA', 'MCM2', 'NapsinA', 'P16', 'P40', 'p53', 'P63', 'PAX2', 'PAX8', 'PCK',
                'PDL1', 'RRM1', 'SATB2', 'Syn', 'TTF1', 'VEGFC', 'Villin', 'Villinco', 'other', 'Ki67',
                'CD516', 'detectTime', 'patNum', 'modification', 'doubt']

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        immunohis_map = {0: '无', 1: '-', 2: '±', 3: '+', 4: '++', 5: '+++', "/": "/"}
        row = np.zeros(0, dtype=str)
        if buffer.get('Immunohis').get(pid) is None or buffer.get('Immunohis').get(pid).get(treIndex) is None:
            row = np.append(row, ['/'] * Immunohis.header_num)
            return row
        obj = buffer.get('Immunohis').get(pid).get(treIndex)
        for column in columns:
            if column == 'Ki67' or column == 'other':
                value = self.filter_none(obj, column)
                value = str(value) + "%" if value != '/' else value
                row = np.append(row, value)
            elif column in ['detectTime', 'patNum']:
                value = self.filter_none(obj, column)
                row = np.append(row, value)
            else:
                value = self.filter_none(obj, column)
                value = immunohis_map.get(value)
                row = np.append(row, value)
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = np.zeros(0, dtype=str)
        for column in columns:
            header = np.append(header, self.export_header_map.get(column))
        Immunohis.header_num = len(header)
        return header


# 病人分子检测信息表
class MoleDetec(Base, ModificationAndDoubt):
    __tablename__ = 'moleDetec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    ALK = Column(Integer, comment='ALK(0-阴性,1-阳性,2-无)')
    BIM = Column(Integer, comment='BIM(0-阴性,1-阳性,2-无)')
    BRAF = Column(Integer, comment='BRAF(0-阴性,1-阳性,2-无)')
    cMET = Column(Integer, comment='cMET(0-阴性,1-阳性,2-无)')
    EGFR = Column(Integer, comment='EGFR(0-阴性,1-阳性,2-无)')
    HER_2 = Column(Integer, comment='HER-2(0-阴性,1-阳性,2-无)')
    KRAS = Column(Integer, comment='KRAS(0-阴性,1-阳性,2-无)')
    PIK3CA = Column(Integer, comment='PIK3CA(0-阴性,1-阳性,2-无)')
    ROS1 = Column(Integer, comment='ROS1(0-阴性,1-阳性,2-无)')
    RET = Column(Integer, comment='RET(0-阴性,1-阳性,2-无)')
    UGT1A1 = Column(Integer, comment='UGT1A1(0-阴性,1-阳性,2-无)')
    NTRK = Column(Integer, comment='UGT1A1(0-阴性,1-阳性,2-无)')

    ALKSam = Column(String(255), comment='ALK检测样本')  # 下面的文本都要改
    BIMSam = Column(String(255), comment='BIM检测样本')
    BRAFSam = Column(String(255), comment='BRAF检测样本')
    cMETSam = Column(String(255), comment='cMET检测样本')
    EGFRSam = Column(String(255), comment='EGFR检测样本')
    HER_2Sam = Column(String(255), comment='HER-2检测样本')
    KRASSam = Column(String(255), comment='KRAS检测样本')
    PIK3CASam = Column(String(255), comment='PIK3CA检测样本')
    ROS1Sam = Column(String(255), comment='ROS1检测样本')
    RETSam = Column(String(255), comment='RET检测样本')
    UGT1A1Sam = Column(String(255), comment='UGT1A1检测样本')
    NTRKSam = Column(String(255), comment='NTRK检测样本')

    ALKDetMed = Column(Integer, comment='ALK检测方法(1-ARMS,2-FISH,3-NGS)')
    BIMDetMed = Column(Integer, comment='BIM检测方法(1-ARMS,2-FISH,3-NGS)')
    BRAFDetMed = Column(Integer, comment='BRAF检测方法(1-ARMS,2-FISH,3-NGS)')
    cMETDetMed = Column(Integer, comment='cMET检测方法(1-ARMS,2-FISH,3-NGS)')
    EGFRDetMed = Column(Integer, comment='EGFR检测方法(1-ARMS,2-FISH,3-NGS)')
    HER_2DetMed = Column(Integer, comment='HER-2检测方法(1-ARMS,2-FISH,3-NGS)')
    KRASDetMed = Column(Integer, comment='KRAS检测方法(1-ARMS,2-FISH,3-NGS)')
    PIK3CADetMed = Column(Integer, comment='PIK3CA检测方法(1-ARMS,2-FISH,3-NGS)')
    ROS1DetMed = Column(Integer, comment='ROS1检测方法(1-ARMS,2-FISH,3-NGS)')
    RETDetMed = Column(Integer, comment='RET检测方法(1-ARMS,2-FISH,3-NGS)')
    UGT1A1DetMed = Column(Integer, comment='UGT1A1检测方法(1-ARMS,2-FISH,3-NGS)')
    NTRKDetMed = Column(Integer, comment='NTRKDetMed检测方法(1-ARMS,2-FISH,3-NGS)')

    ALKDesc = Column(String(255), comment='ALK结果描述')
    BIMDesc = Column(String(255), comment='BIM结果描述')
    BRAFDesc = Column(String(255), comment='BRAF结果描述')
    cMETDesc = Column(String(255), comment='cMET结果描述')
    EGFRDesc = Column(String(255), comment='EGFR结果描述')
    HER_2Desc = Column(String(255), comment='HER-2结果描述')
    KRASDesc = Column(String(255), comment='KRAS结果描述')
    PIK3CADesc = Column(String(255), comment='PIK3CA结果描述')
    ROS1Desc = Column(String(255), comment='ROS1结果描述')
    RETDesc = Column(String(255), comment='RET结果描述')
    UGT1A1Desc = Column(String(255), comment='UGT1A1结果描述')
    NTRKDesc = Column(String(255), comment='NTRK结果描述')

    path = Column(String(200), comment='报告文件路径')
    MSI = Column(Integer, comment='MSI 0-MSS,1-MSIH,2-MSIL')
    other = Column(Text)
    PDL1 = Column(Float, comment='PD-L1表达 0-未测,1-不详,2->50%,3-1%-50%,4-<1%,5-阴性')
    PDL1KT = Column(String(255), comment='PDL1抗体')
    PD1 = Column(Float, comment='PD1表达 0-未测,1-不详,2->50%,3-1%-50%,4-<1%,5-阴性')
    PD1KT = Column(String(255), comment='PD1抗体')

    TMB = Column(String(20), comment='TMB')  # ???
    detectTime = Column(Date, comment='检测时间')
    detectCompany = Column(String(255), comment='检测公司')
    sampleType = Column(String(255), comment='样本类型')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {
        'MSI': 'MSI', 'PD1': 'PD-1表达', 'PD1KT': 'PD1KT', 'PDL1': 'PD-L1表达', 'PDL1KT': 'PDL1KT', 'TMB': 'TMB',
        'other': '其他', 'detectTime': '分子检测检测时间', 'detectCompany': '检测公司', 'sampleType': '样本类型',
        'EGFR': 'EGFR', 'ALK': 'ALK', 'ROS1': 'ROS1', 'HER_2': 'HER_2', 'BRAF': 'BRAF',
        'cMET': 'cMET', 'RET': 'RET', 'NTRK': 'NTRK', 'KRAS': 'KRAS', 'BIM': 'BIM',
        'PIK3CA': 'PIK3CA', 'UGT1A1': 'UGT1A1',
        'EGFRSam': 'EGFR检测样本', 'ALKSam': 'ALK检测样本', 'ROS1Sam': 'ROS1检测样本', 'HER_2Sam': 'HER_2检测样本',
        'BRAFSam': 'BRAF检测样本',
        'cMETSam': 'cMET检测样本', 'RETSam': 'RET检测样本', 'NTRKSam': 'NTRK检测样本', 'KRASSam': 'KRAS检测样本', 'BIMSam': 'BIM检测样本',
        'PIK3CASam': 'PIK3CA检测样本', 'UGT1A1Sam': 'UGT1A1检测样本',
        'EGFRMed': 'EGFR检测方法', 'ALKMed': 'ALK检测方法', 'ROS1Med': 'ROS1检测方法', 'HER_2Med': 'HER_2检测方法',
        'BRAFMed': 'BRAF检测方法',
        'cMETMed': 'cMET检测方法', 'RETMed': 'RET检测方法', 'NTRKMed': 'NTRK检测方法', 'KRASMed': 'KRAS检测方法', 'BIMMed': 'BIM检测方法',
        'PIK3CAMed': 'PIK3CA检测方法', 'UGT1A1Med': 'UGT1A1检测方法',
        'EGFRDesc': 'EGFR结果描述', 'ALKDesc': 'ALK结果描述', 'ROS1Desc': 'ROS1结果描述', 'HER_2Desc': 'HER_2结果描述',
        'BRAFDesc': 'BRAF结果描述',
        'cMETDesc': 'cMET结果描述', 'RETDesc': 'RET结果描述', 'NTRKDesc': 'NTRK结果描述', 'KRASDesc': 'KRAS结果描述',
        'BIMDesc': 'BIM结果描述',
        'PIK3CADesc': 'PIK3CA结果描述', 'UGT1A1Desc': 'UGT1A1结果描述'
    }

    def keys(self):
        return ['id', 'pid', 'treNum', 'ALK', 'BIM', 'BRAF', 'cMET', 'EGFR', 'HER_2', 'KRAS', 'NTRK',
                'PIK3CA', 'ROS1', 'RET', 'UGT1A1', 'ALKSam', 'BIMSam', 'BRAFSam', 'cMETSam', 'EGFRSam', 'HER_2Sam',
                'KRASSam', 'PIK3CASam', 'ROS1Sam', 'NTRKSam',
                'RETSam', 'UGT1A1Sam', 'ALKDetMed', 'BIMDetMed', 'BRAFDetMed', 'cMETDetMed', 'EGFRDetMed',
                'HER_2DetMed', 'KRASDetMed', 'PIK3CADetMed', 'ROS1DetMed', 'NTRKDetMed',
                'RETDetMed', 'UGT1A1DetMed', 'ALKDesc', 'BIMDesc', 'BRAFDesc', 'cMETDesc', 'EGFRDesc', 'HER_2Desc',
                'KRASDesc', 'PIK3CADesc',
                'ROS1Desc', 'RETDesc', 'UGT1A1Desc', 'NTRKDesc', 'path', 'MSI', 'other', 'PDL1', 'PDL1KT', 'TMB', 'PD1',
                'PD1KT', 'sampleType', 'detectTime', 'detectCompany', 'modification', 'doubt']

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        moleDetec_map = {0: '阴性', 1: '阳性', 2: '无', "/": "/"}
        moleDetec_DetMed_map = {1: 'ARMS', 2: 'FISH', 3: 'NGS', "/": "/"}
        moleDetec_MSI_map = {0: 'MSS', 1: 'MSIH', 2: 'MSIL', "/": "/"}
        moleDetec_fields = ['ALK', 'BIM', 'BRAF', 'cMET', 'EGFR', 'HER_2', 'KRAS',
                            'PIK3CA', 'ROS1', 'RET', 'UGT1A1', 'NTRK']
        row = np.zeros(0, dtype=str)
        if buffer.get('MoleDetec').get(pid) is None or buffer.get('MoleDetec').get(pid).get(treIndex) is None:
            row = np.append(row, ['/'] * MoleDetec.header_num)
            return row
        obj = buffer.get('MoleDetec').get(pid).get(treIndex)
        for column in columns:
            if column in moleDetec_fields:
                value = self.filter_none(obj, column)
                value = moleDetec_map.get(value)
                row = np.append(row, value)
                if value == '阳性':
                    valueSam = self.filter_none(obj, column + 'Sam')
                    valueDetMed = self.filter_none(obj, column + 'DetMed')
                    valueDetMed = moleDetec_DetMed_map.get(valueDetMed)
                    valueDesc = self.filter_none(obj, column + 'Desc')
                    row = np.append(row, [valueSam, valueDetMed, valueDesc])
                else:
                    row = np.append(row, ['/', '/', '/'])
            elif column == 'MSI':
                value = self.filter_none(obj, column)
                value = moleDetec_MSI_map.get(value)
                row = np.append(row, value)
            elif column == 'PD1' or column == 'PDL1':
                value = self.filter_none(obj, column)
                value = str(value) + "%" if value != '/' else value
                row = np.append(row, value)
            else:
                value = self.filter_none(obj, column)
                row = np.append(row, value)
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = np.zeros(0, dtype=str)
        for column in columns:
            if column in ['MSI', 'PD1', 'PD1KT', 'PDL1', 'PDL1KT', 'TMB',
                          'other', 'detectTime', 'detectCompany', 'sampleType']:
                header = np.append(header, self.export_header_map.get(column))
            else:
                header = np.append(header, [self.export_header_map.get(column),
                                            self.export_header_map.get(column) + '检测样本',
                                            self.export_header_map.get(column) + '检测方法',
                                            self.export_header_map.get(column) + '检测描述'])
        MoleDetec.header_num = len(header)
        return header


# 症状体征表
class Signs(Base, ModificationAndDoubt):
    __tablename__ = 'signs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    symName = Column(String(255), comment='症状名称')
    begDate = Column(DateTime, comment='开始日期')
    isExe = Column(Integer, comment='目前是否存在')
    endDate = Column(DateTime, comment='结束日期')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'symName': '症状名称', 'begDate': '开始日期',
                         'isExe': '目前是否存在', 'endDate': '结束日期'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        isExe_map = {0: '否', 1: '是', '/': '/'}
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('Signs').get(pid) is None or buffer.get('Signs').get(pid).get(treIndex) is None:
            # row.extend(['/'] * Signs.header_num)
            row = np.append(row, ['/'] * Signs.header_num)
            return row
        obj_array = buffer.get('Signs').get(pid).get(treIndex)

        for obj in obj_array:
            for column in columns:
                if column == 'isExe':
                    value = self.filter_none(obj, column)
                    value = isExe_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'endDate':
                    value_isExe = self.filter_none(obj, 'isExe')
                    if value_isExe == 0:
                        value = self.filter_none(obj, column)
                    else:
                        value = '/'
                    # row.append(value)
                    row = np.append(row, value)
                else:
                    value = self.filter_none(obj, column)
                    # row.append(value)
                    row = np.append(row, value)
        # row.extend(['/'] * (Signs.header_num - len(row)))
        row = np.append(row, ['/'] * (Signs.header_num - len(row)))
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        # header = []
        header = np.zeros(0, dtype=str)
        # 求最多有多少条
        max_num = 0
        for value1 in buffer.get('Signs').values():
            for value2 in value1.values():
                num = len(value2)
                if num > max_num:
                    max_num = num

        if max_num > 1:
            header_num = max_num
        else:
            header_num = 1

        for i in range(1, header_num + 1):
            for column in columns:
                # header.append(self.export_header_map.get(column) + str(i))
                header = np.append(header, self.export_header_map.get(column) + str(i))
        Signs.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'symName', 'begDate', 'isExe', 'endDate',
                'modification', 'doubt']


# 副反应表
class SideEffect(Base, ModificationAndDoubt):
    __tablename__ = 'sideEffect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    sidReaName = Column(String(255), comment='副反应名称')
    sidReaNameOther = Column(String(2048), comment='副反应其他名称')  # 随访数据库好像没有这字段了
    sidRecCla = Column(Integer, comment='副反应分级')
    begDate = Column(Date, comment='开始日期')
    isExe = Column(Integer, comment='目前是否存在')
    treatment = Column(String(2048), comment='治疗情况')
    endDate = Column(Date, comment='结束日期')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'sidReaName': '症状描述', 'sidRecCla': '副反应分级', 'begDate': '开始日期',
                         'isExe': '目前是否存在', 'endDate': '结束日期', 'treatment': '治疗情况'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        isExe_map = {0: '否', 1: '是', '/': '/'}
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('SideEffect').get(pid) is None or buffer.get('SideEffect').get(pid).get(treIndex) is None:
            # row.extend(['/'] * SideEffect.header_num)
            row = np.append(row, ['/'] * SideEffect.header_num)
            return row
        obj_array = buffer.get('SideEffect').get(pid).get(treIndex)

        for obj in obj_array:
            for column in columns:
                if column == 'isExe':
                    value = self.filter_none(obj, column)
                    value = isExe_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'endDate':
                    value_isExe = self.filter_none(obj, 'isExe')
                    if value_isExe == 0:
                        value = self.filter_none(obj, column)
                    else:
                        value = '/'
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'sidReaName':
                    value = self.filter_none(obj, column)
                    if value == '其他副作用_其他':
                        sidReaNameOther_value = self.filter_none(obj, 'sidReaNameOther')
                        value = '其他副作用_' + sidReaNameOther_value
                    elif value == '骨髓抑制_其他':
                        sidReaNameOther_value = self.filter_none(obj, 'sidReaNameOther')
                        value = '骨髓抑制_' + sidReaNameOther_value
                    # row.append(value)
                    row = np.append(row, value)
                else:
                    value = self.filter_none(obj, column)
                    # row.append(value)
                    row = np.append(row, value)
        # row.extend(['/'] * (SideEffect.header_num - len(row)))
        row = np.append(row, ['/'] * (SideEffect.header_num - len(row)))
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        # header = []
        header = np.zeros(0, dtype=str)
        # 求最多有多少条
        max_num = 0
        for value1 in buffer.get('SideEffect').values():
            for value2 in value1.values():
                num = len(value2)
                if num > max_num:
                    max_num = num
        header_num = max_num if max_num > 1 else 1

        for i in range(1, header_num + 1):
            for column in columns:
                # header.append(self.export_header_map.get(column) + str(i))
                header = np.append(header, self.export_header_map.get(column) + str(i))
        SideEffect.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'sidReaName', 'sidRecCla', 'begDate', 'isExe', 'treatment', 'endDate',
                'sidReaNameOther', 'modification', 'doubt']
