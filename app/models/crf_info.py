from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base, ModificationAndDoubt
import numpy as np


# 随访信息表
class FollInfo(Base, ModificationAndDoubt):
    __tablename__ = 'follInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    number = Column(Integer, comment='第n条记录')
    date = Column(DateTime, comment='时间')  # date
    effEva = Column(Integer, comment='疗效评估,1 : PD-进展, 2 : SD-稳定, 3 : PR-部分缓解, 4 : CR-完全缓解, 5 : 术后未发现新病灶')
    folMet = Column(Integer, comment='随访方式,1 : 电话, 2 : 门诊, 3 : 住院')
    livSta = Column(Integer, comment='生存状态, 1 : 死亡, 2 : 存活, 3 : 失联')
    dieDate = Column(Date, comment='死亡日期')
    remarks = Column(String(1000), comment='备注')
    imaFilType = Column(Integer, comment='影像文件类型, 1 : X光, 2 : 超声, 3 : CT, 4 : MRI, 5 : PET/CT')
    suv = Column(Float, comment='选择PET影像时记录其标准摄取值(standard uptake value ,SUV)')
    savFilPath = Column(String(200), comment='保存文件路径,多个以逗号分隔')
    examArea = Column(String(20), comment='检查部位')  # 废弃
    tumorLD = Column(Float, comment='肿瘤长径')  # 废弃
    tumorSD = Column(Float, comment='肿瘤短径')  # 废弃
    tumorDesc = Column(String(100), comment='肿瘤描述')  # 废弃

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')
    module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')

    # 和导出功能有关
    export_header_map = {'nextFollowupTime': '计划下次随访时间', 'date': '随访日期', 'folMet': '随访方式', 'effEva': '疗效评估',
                         'livSta': '生存状态', 'dieDate': '死亡时间', 'imaFilType': '影像类型', 'remarks': '备注'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex, follInfoNum):
        folMet_map = {1: '电话', 2: '门诊', 3: '住院', '/': '/'}
        effEva_map = {1: 'PD-进展', 2: 'SD-稳定', 3: 'PR-部分缓解',
                      4: 'CR-完全缓解', 5: '术后未发现新病灶', '/': '/'}
        livSta_map = {1: '死亡', 2: '存活', 3: '失联', '/': '/'}
        imaFilType_map = {1: 'X光', 2: '超声', 3: 'CT', 4: 'MRI', 5: 'PET/CT', '/': '/',
                          '1': 'X光', '2': '超声', '3': 'CT', '4': 'MRI', '5': 'PET/CT'}
        nextFollowupTime_flag = False
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('FollInfo').get(pid) is None:
            # row.extend(['/']*FollInfo.header_num)
            row = np.append(row, ['/'] * FollInfo.header_num)
            return row
        obj_array = buffer.get('FollInfo').get(pid)
        obj_array_size = len(obj_array)
        if buffer.get('Patient').get(pid) is None:
            patient_obj = None
        else:
            patient_obj = buffer.get('Patient').get(pid)

        num = obj_array_size if obj_array_size < follInfoNum else follInfoNum

        for k in range(0, num):
            for column in columns:
                if column == 'folMet':
                    value = self.filter_none(obj_array[k], column)
                    value = folMet_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'effEva':
                    value = self.filter_none(obj_array[k], column)
                    value = effEva_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'livSta':
                    value = self.filter_none(obj_array[k], column)
                    value = livSta_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'dieDate':
                    livSta = self.filter_none(obj_array[k], 'livSta')
                    livSta = livSta_map.get(livSta)
                    if livSta == '死亡':
                        value = str(obj_array[k].dieDate) if obj_array[k].dieDate else '/'
                    else:
                        value = '/'
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'imaFilType':
                    value = self.filter_none(obj_array[k], column)
                    value = imaFilType_map.get(value)
                    # row.append(value)
                    row = np.append(row, value)
                elif column == 'nextFollowupTime':
                    if not nextFollowupTime_flag:
                        value = self.filter_none(patient_obj, column) if patient_obj else '/'
                        # row.append(value)
                        row = np.append(row, value)
                        nextFollowupTime_flag = True
                else:
                    value = self.filter_none(obj_array[k], column)
                    # row.append(value)
                    row = np.append(row, value)
        # row.extend(['/']*(FollInfo.header_num - len(row)))
        row = np.append(row, ['/'] * (FollInfo.header_num - len(row)))

        return row

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer, follInfoNum):
        nextFollowupTime_flag = False
        # header = []
        header = np.zeros(0, dtype=str)
        for i in range(1, follInfoNum + 1):
            for column in columns:
                if column == 'nextFollowupTime':
                    if not nextFollowupTime_flag:
                        # header.append(self.export_header_map.get(column))
                        header = np.append(header, self.export_header_map.get(column))
                        nextFollowupTime_flag = True
                else:
                    # header.append(self.export_header_map.get(column) + str(i))
                    header = np.append(header, self.export_header_map.get(column) + str(i))
        FollInfo.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'number', 'date', 'effEva', 'folMet', 'livSta', 'dieDate', 'remarks', 'imaFilType', 'suv',
                'examArea', 'examArea', 'tumorLD', 'tumorSD', 'tumorDesc', 'modification', 'doubt', 'module_status']
