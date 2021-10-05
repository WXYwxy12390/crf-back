from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
import numpy as np
from app.models.base import Base


# 肺功能表
class Lung(Base):
    __tablename__ = 'lung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='检测时间')
    FVC_exp = Column(Float, comment='用力肺活量(L)预期值')
    FEV1_FVC_exp = Column(Float, comment='用力呼气一秒率(%)预期值')
    MEF_exp = Column(Float, comment='用力呼气中期流速(L/S)预期值')
    MEF25_exp = Column(Float, comment='25%用力呼气流速(L/S)预期值')
    MEF50_exp = Column(Float, comment='50%用力呼气流速(L/S)预期值')
    MEF75_exp = Column(Float, comment='75%用力呼气流速(L/S)预期值')
    TLC_sb_exp = Column(Float, comment='肺总量(L)预期值')
    RV_exp = Column(Float, comment='残气容积(L)预期值')
    RV_TLC_exp = Column(Float, comment='残气容积/肺总量比(%)预期值')
    VC_exp = Column(Float, comment='肺活量(L)预期值')
    DLCO_ex_exp = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)预期值')
    DLCO_sb_exp = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)预期值')
    KCO_exp = Column(Float, comment='比弥散量预期值')
    FVC_best = Column(Float, comment='用力肺活量(L)最佳值')
    FEV1_FVC_best = Column(Float, comment='用力呼气一秒率(%)最佳值')
    MEF_best = Column(Float, comment='用力呼气中期流速(L/S)最佳值')
    MEF25_best = Column(Float, comment='25%用力呼气流速(L/S)最佳值')
    MEF50_best = Column(Float, comment='50%用力呼气流速(L/S)最佳值')
    MEF75_best = Column(Float, comment='75%用力呼气流速(L/S)最佳值')
    TLC_sb_best = Column(Float, comment='肺总量(L)最佳值')
    RV_best = Column(Float, comment='残气容积(L)最佳值')
    RV_TLC_best = Column(Float, comment='残气容积/肺总量比(%)最佳值')
    VC_best = Column(Float, comment='肺活量(L)最佳值')
    DLCO_ex_best = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)最佳值')
    DLCO_sb_best = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)最佳值')
    KCO_best = Column(Float, comment='比弥散量最佳值')
    FVC_ratio = Column(Float, comment='用力肺活量(L)最佳值/预期值(%)')
    FEV1_FVC_ratio = Column(Float, comment='用力呼气一秒率(%)最佳值/预期值(%)')
    MEF_ratio = Column(Float, comment='用力呼气中期流速(L/S)最佳值/预期值(%)')
    MEF25_ratio = Column(Float, comment='25%用力呼气流速(L/S)最佳值/预期值(%)')
    MEF50_ratio = Column(Float, comment='50%用力呼气流速(L/S)最佳值/预期值(%)')
    MEF75_ratio = Column(Float, comment='75%用力呼气流速(L/S)最佳值/预期值(%)')
    TLC_sb_ratio = Column(Float, comment='肺总量(L)最佳值/预期值(%)')
    RV_ratio = Column(Float, comment='残气容积(L)最佳值/预期值(%)')
    RV_TLC_ratio = Column(Float, comment='残气容积/肺总量比(%)最佳值/预期值(%)')
    VC_ratio = Column(Float, comment='肺活量(L)最佳值/预期值(%)')
    DLCO_ex_ratio = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)最佳值/预期值(%)')
    DLCO_sb_ratio = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)最佳值/预期值(%)')
    KCO_ratio = Column(Float, comment='比弥散量最佳值/预期值(%)')
    FVCMea = Column(Integer, comment='用力肺活量(L)临床意义判定')
    FEV1_FVCMea = Column(Integer, comment='用力呼气一秒率(%)临床意义判定')
    MEFMea = Column(Integer, comment='用力呼气中期流速(L/S)临床意义判定')
    MEF25Mea = Column(Integer, comment='25%用力呼气流速(L/S)临床意义判定')
    MEF50Mea = Column(Integer, comment='50%用力呼气流速(L/S)临床意义判定')
    MEF75Mea = Column(Integer, comment='75%用力呼气流速(L/S)临床意义判定')
    TLC_sbMea = Column(Integer, comment='肺总量(L)临床意义判定')
    RVMea = Column(Integer, comment='残气容积(L)临床意义判定')
    RV_TLCMea = Column(Integer, comment='残气容积/肺总量比(%)临床意义判定')
    VCMea = Column(Integer, comment='肺活量(L)临床意义判定')
    DLCO_exMea = Column(Integer, comment='无需屏气弥散(mL/mmHg/Mi)临床意义判定')
    DLCO_sbMea = Column(Integer, comment='肺一氧化碳弥散量(mL/mmHg/Mi)临床意义判定')
    KCOMea = Column(Integer, comment='比弥散量临床意义判定')
    FVCNote = Column(Text(10000), comment='用力肺活量(L)备注')
    FEV1_FVCNote = Column(Text(10000), comment='用力呼气一秒率(%)备注')
    MEFNote = Column(Text(10000), comment='用力呼气中期流速(L/S)备注')
    MEF25Note = Column(Text(10000), comment='25%用力呼气流速(L/S)备注')
    MEF50Note = Column(Text(10000), comment='50%用力呼气流速(L/S)备注')
    MEF75Note = Column(Text(10000), comment='75%用力呼气流速(L/S)备注')
    TLC_sbNote = Column(Text(10000), comment='肺总量(L)备注')
    RVNote = Column(Text(10000), comment='残气容积(L)备注')
    RV_TLCNote = Column(Text(10000), comment='残气容积/肺总量比(%)备注')
    VCNote = Column(Text(10000), comment='肺活量(L)备注')
    DLCO_exNote = Column(Text(10000), comment='无需屏气弥散(mL/mmHg/Mi)备注')
    DLCO_sbNote = Column(Text(10000), comment='肺一氧化碳弥散量(mL/mmHg/Mi)备注')
    KCONote = Column(Text(10000), comment='比弥散量备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    query_reply = Column(JSON, comment='质疑和回复')
    module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')

    # 和导出功能有关
    export_header_map = {'samplingTime': '肺功能检查时间', 'FVC': 'FVC(L)', 'FEV1_FVC': 'FEV1/FVC(%)', 'MEF': 'MEF(L/S)',
                         'MEF25': 'MEF25(L/S)', 'MEF50': 'MEF50(L/S)', 'MEF75': 'MEF75(L/S)', 'TLC_sb': 'TLC’sb(L)',
                         'RV': 'RV(L)', 'RV_TLC': 'RV’/TLC’(%)', 'VC': 'VC(L)', 'DLCO_ex': 'DLCO-ex(mL/mmHg/Mi)',
                         'DLCO_sb': 'DLCO-sb(mL/mmHg/Mi)', 'KCO': 'KCO',
                         'FVC_exp': 'FVC(L)预期值', 'FEV1_FVC_exp': 'FEV1/FVC(%)预期值', 'MEF_exp': 'MEF(L/S)预期值',
                         'MEF25_exp': 'MEF25(L/S)预期值', 'MEF50_exp': 'MEF50(L/S)预期值', 'MEF75_exp': 'MEF75(L/S)预期值', 'TLC_sb_exp': 'TLC’sb(L)预期值',
                         'RV_exp': 'RV(L)预期值', 'RV_TLC_exp': 'RV’/TLC’(%)预期值', 'VC_exp': 'VC(L)预期值', 'DLCO_ex_exp': 'DLCO-ex(mL/mmHg/Mi)预期值',
                         'DLCO_sb_exp': 'DLCO-sb(mL/mmHg/Mi)预期值', 'KCO_exp': 'KCO预期值',
                         'FVC_best': 'FVC(L)最佳值', 'FEV1_FVC_best': 'FEV1/FVC(%)最佳值', 'MEF_best': 'MEF(L/S)最佳值',
                         'MEF25_best': 'MEF25(L/S)最佳值', 'MEF50_best': 'MEF50(L/S)最佳值', 'MEF75_best': 'MEF75(L/S)最佳值', 'TLC_sb_best': 'TLC’sb(L)最佳值',
                         'RV_best': 'RV(L)最佳值', 'RV_TLC_best': 'RV’/TLC’(%)最佳值', 'VC_best': 'VC(L)最佳值', 'DLCO_ex_best': 'DLCO-ex(mL/mmHg/Mi)最佳值',
                         'DLCO_sb_best': 'DLCO-sb(mL/mmHg/Mi)最佳值', 'KCO_best': 'KCO最佳值',
                         'FVC_ratio': 'FVC(L)最佳值/预期值(%)', 'FEV1_FVC_ratio': 'FEV1/FVC(%)最佳值/预期值(%)', 'MEF_ratio': 'MEF(L/S)最佳值/预期值(%)',
                         'MEF25_ratio': 'MEF25(L/S)最佳值/预期值(%)', 'MEF50_ratio': 'MEF50(L/S)最佳值/预期值(%)', 'MEF75_ratio': 'MEF75(L/S)最佳值/预期值(%)', 'TLC_sb_ratio': 'TLC’sb(L)最佳值/预期值(%)',
                         'RV_ratio': 'RV(L)最佳值/预期值(%)', 'RV_TLC_ratio': 'RV’/TLC’(%)最佳值/预期值(%)', 'VC_ratio': 'VC(L)最佳值/预期值(%)', 'DLCO_ex_ratio': 'DLCO-ex(mL/mmHg/Mi)最佳值/预期值(%)',
                         'DLCO_sb_ratio': 'DLCO-sb(mL/mmHg/Mi)最佳值/预期值(%)', 'KCO_ratio': 'KCO最佳值/预期值(%)',
                         'FVCMea': 'FVC(L)临床意义判定', 'FEV1_FVCMea': 'FEV1/FVC(%)临床意义判定', 'MEFMea': 'MEF(L/S)临床意义判定',
                         'MEF25Mea': 'MEF25(L/S)临床意义判定', 'MEF50Mea': 'MEF50(L/S)临床意义判定', 'MEF75Mea': 'MEF75(L/S)临床意义判定', 'TLC_sbMea': 'TLC’sb(L)临床意义判定',
                         'RVMea': 'RV(L)临床意义判定', 'RV_TLCMea': 'RV’/TLC’(%)临床意义判定', 'VCMea': 'VC(L)临床意义判定', 'DLCO_exMea': 'DLCO-ex(mL/mmHg/Mi)临床意义判定',
                         'DLCO_sbMea': 'DLCO-sb(mL/mmHg/Mi)临床意义判定', 'KCOMea': 'KCO临床意义判定',
                         'FVCNote': 'FVC(L)备注', 'FEV1_FVCNote': 'FEV1/FVC(%)备注', 'MEFNote': 'MEF(L/S)备注',
                         'MEF25Note': 'MEF25(L/S)备注', 'MEF50Note': 'MEF50(L/S)备注', 'MEF75Note': 'MEF75(L/S)备注', 'TLC_sbNote': 'TLC’sb(L)备注',
                         'RVNote': 'RV(L)备注', 'RV_TLCNote': 'RV’/TLC’(%)备注', 'VCNote': 'VC(L)备注', 'DLCO_exNote': 'DLCO-ex(mL/mmHg/Mi)备注',
                         'DLCO_sbNote': 'DLCO-sb(mL/mmHg/Mi)备注', 'KCONote': 'KCO备注'
                         }

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        Mea_map = {-1: '异常', 0: '正常', 1: '异常 1', 2: '异常 2', 3: '异常 3', 4: '异常 4', 5: '异常 5', "/": "/"}
        row = []
        # row = np.zeros(0, dtype=str)
        if buffer.get('Lung').get(pid) is None or buffer.get('Lung').get(pid).get(treIndex) is None:
            # row.extend(['/'] * Lung.header_num)
            row = np.append(row, ['/']*Lung.header_num)
            return row

        obj = buffer.get('Lung').get(pid).get(treIndex)
        for column in columns:
            if column == 'samplingTime':
                value = self.filter_none(obj, column)
                # row.append(value)
                row = np.append(row, value)
            else:
                value_exp = self.filter_none(obj, column + '_exp')
                value_best = self.filter_none(obj, column + '_best')
                value_ratio = self.filter_none(obj, column + '_ratio')
                value_ratio = str(value_ratio) + "%" if value_ratio != "/" else value_ratio
                value_Mea = Mea_map.get(self.filter_none(obj, column + 'Mea'))
                value_Note = self.filter_none(obj, column + 'Note')
                # row.extend([value_exp, value_best, value_ratio, value_Mea, value_Note])
                row = np.append(row, [value_exp, value_best, value_ratio, value_Mea, value_Note])
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        # header = []
        header = np.zeros(0, dtype=str)
        for column in columns:
            if column == 'samplingTime':
                # header.append(self.export_header_map.get(column))
                header = np.append(header, self.export_header_map.get(column))
            else:
                # header.extend([self.export_header_map.get(column) + '预计值',
                #                self.export_header_map.get(column) + '最佳值',
                #                self.export_header_map.get(column) + '最佳值/预计值(%)',
                #                self.export_header_map.get(column) + '临床意义判断',
                #                self.export_header_map.get(column) + '备注'])
                header = np.append(header, [self.export_header_map.get(column) + '预计值',
                                            self.export_header_map.get(column) + '最佳值',
                                            self.export_header_map.get(column) + '最佳值/预计值(%)',
                                            self.export_header_map.get(column) + '临床意义判断',
                                            self.export_header_map.get(column) + '备注'])
        Lung.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'FVC_exp', 'FEV1_FVC_exp', 'MEF_exp', 'MEF25_exp', 'MEF50_exp',
                'MEF75_exp', 'TLC_sb_exp', 'RV_exp', 'RV_TLC_exp', 'VC_exp', 'DLCO_ex_exp', 'DLCO_sb_exp', 'KCO_exp',
                'FVC_best',
                'FEV1_FVC_best', 'MEF_best', 'MEF25_best', 'MEF50_best', 'MEF75_best', 'TLC_sb_best', 'RV_best',
                'RV_TLC_best',
                'VC_best', 'DLCO_ex_best', 'DLCO_sb_best', 'KCO_best', 'FVC_ratio', 'FEV1_FVC_ratio', 'MEF_ratio',
                'MEF25_ratio', 'MEF50_ratio',
                'MEF75_ratio', 'TLC_sb_ratio', 'RV_ratio', 'RV_TLC_ratio', 'VC_ratio', 'DLCO_ex_ratio', 'DLCO_sb_ratio',
                'KCO_ratio',
                'FVCMea', 'FEV1_FVCMea', 'MEFMea', 'MEF25Mea', 'MEF50Mea', 'MEF75Mea', 'TLC_sbMea', 'RVMea',
                'RV_TLCMea', 'VCMea', 'DLCO_exMea',
                'DLCO_sbMea', 'KCOMea', 'FVCNote', 'FEV1_FVCNote', 'MEFNote', 'MEF25Note', 'MEF50Note', 'MEF75Note',
                'TLC_sbNote',
                'RVNote', 'RV_TLCNote', 'VCNote', 'DLCO_exNote', 'DLCO_sbNote', 'KCONote', 'filePath']


# 其他检查表
class OtherExams(Base):
    __tablename__ = 'otherExams'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    ECGDetTime = Column(Date, comment='12导联心电图检测时间')
    ECGDesc = Column(Text, comment='12导联心电图结果描述')  # 长度
    ECGPath = Column(String(200), comment='12导联心电图报告路径,多个以逗号分隔')
    UCGDetTime = Column(Date, comment='超声心动图检测时间')
    UCGDesc = Column(Text, comment='超声心动图结果描述')  # 长度
    UCGPath = Column(String(200), comment='超声心动图报告路径,多个以逗号分隔')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    query_reply = Column(JSON, comment='质疑和回复')
    module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')

    # 和导出功能有关
    export_header_map = {'ECGDetTime': '12导联心电图检测时间', 'ECGDesc': '12导联心电图结果描述',
                         'UCGDetTime': '超声心动图检测时间', 'UCGDesc': '超声心动图结果描述'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('OtherExams').get(pid) is None or buffer.get('OtherExams').get(pid).get(treIndex) is None:
            # row.extend(['/'] * OtherExams.header_num)
            row = np.append(row, ['/'] * OtherExams.header_num)
            return row
        obj = buffer.get('OtherExams').get(pid).get(treIndex)
        for column in columns:
            value = self.filter_none(obj, column)
            # row.append(value)
            row = np.append(row, value)
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        # header = []
        header = np.zeros(0, dtype=str)
        for column in columns:
            # header.append(self.export_header_map.get(column))
            header = np.append(header, self.export_header_map.get(column))
        OtherExams.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'treNum', 'ECGDetTime', 'ECGDesc', 'ECGPath', 'UCGDetTime', 'UCGDesc', 'UCGPath']


# 影像学检查表
class ImageExams(Base):
    __tablename__ = 'ImageExams'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    detectTime = Column(Date, comment='检测时间')
    examArea = Column(String(255), comment='检查部位')
    photoNumber = Column(String(255), comment='影像号')
    exmaMethod = Column(String(255), comment='检查方法')
    tumorLD = Column(Float, comment='肿瘤长径')
    tumorSD = Column(Float, comment='肿瘤短径')
    tumorDesc = Column(Text, comment='肿瘤描述')
    path = Column(String(200), comment='文件路径,多个以逗号分隔')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    query_reply = Column(JSON, comment='质疑和回复')
    module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')

    # 和导出功能有关
    export_header_map = {'detectTime': '影像学检查检测时间', 'examArea': '检查部位', 'exmaMethod': '检查方法',
                         'tumorLD': '肿瘤长径', 'tumorSD': '肿瘤短径', 'tumorDesc': '肿瘤描述', 'photoNumber':'影像号'}

    def keys(self):
        return ['id','pid','treNum','detectTime','examArea','exmaMethod','tumorLD','tumorSD','tumorDesc','path','photoNumber']

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        row = np.zeros(0, dtype=str)
        if buffer.get('ImageExams').get(pid) is None or buffer.get('ImageExams').get(pid).get(treIndex) is None:
            row = np.append(row, ['/'] * ImageExams.header_num)
            return row
        obj_array = buffer.get('ImageExams').get(pid).get(treIndex)

        for obj in obj_array:
            for column in columns:
                value = self.filter_none(obj, column)
                row = np.append(row, value)
        row = np.append(row, ['/'] * (ImageExams.header_num - len(row)))
        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = np.zeros(0, dtype=str)
        # 求最多有多少条
        max_num = 0
        for value1 in buffer.get('ImageExams').values():
            for value2 in value1.values():
                num = len(value2)
                if num > max_num:
                    max_num = num
        header_num = max_num if max_num > 1 else 1

        for i in range(1, header_num + 1):
            for column in columns:
                header = np.append(header, self.export_header_map.get(column) + str(i))
        ImageExams.header_num = len(header)
        return header
