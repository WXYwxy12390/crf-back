from flask import make_response
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.writer.excel import save_virtual_workbook

from app.models.base_line import DrugHistory
from app.models.therapy_record import DetailTrePlan


class Export:
    # 缓存数据
    buffer = {}

    base_line_table = ['Patient','PastHis','IniDiaPro','BloodRoutine', 'BloodBio', 'Thyroid', 'Coagulation', 'MyocardialEnzyme',
                        'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker','Lung', 'OtherExams', 'ImageExams',
                       'Immunohis','MoleDetec']
    trement_info_table = ['TreRec','OneToFive','Surgery','Radiotherapy','BloodRoutine', 'BloodBio', 'Thyroid',
                          'Coagulation', 'MyocardialEnzyme','Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker','Lung',
                          'OtherExams', 'ImageExams','Immunohis','MoleDetec','Signs','SideEffect']
    lab_inspectation_table = ['BloodRoutine', 'BloodBio', 'Thyroid', 'Coagulation', 'MyocardialEnzyme',
                              'Cytokines', 'LymSubsets', 'UrineRoutine', 'TumorMarker']
    other_inspect_table = ['Lung', 'OtherExams', 'ImageExams']

    def __init__(self, pids, treNums, tables, columns):
        self.pids = pids
        self.treNums = treNums
        self.tables = tables
        self.columns = columns
        self.baseLineTable = []
        self.baseLineColumns = []
        self.trementInfoTable = []
        self.trementInfoColumns = []

        i = 0
        for obj_class_name in self.tables:
            name = obj_class_name.__name__
            if name in Export.base_line_table:
                self.baseLineTable.append(obj_class_name)
                self.baseLineColumns.append(self.columns[i])
            if name in Export.trement_info_table:
                self.trementInfoTable.append(obj_class_name)
                self.trementInfoColumns.append(self.columns[i])
            i += 1

        self.__init_buffer()
        print(self.buffer)
        self.headers = []

    def work(self):
        '''
        i = 0
        for obj_class_name in self.tables:
            obj = obj_class_name()
            self.headers.extend(obj.get_export_header(self.columns[i], self.buffer))
            i += 1
        '''
        for treNum in self.treNums:
            if treNum == 0:
                i = 0
                for obj_class_name in self.baseLineTable:
                    obj = obj_class_name()
                    self.headers.extend(obj.get_export_header(self.baseLineColumns[i], self.buffer))
                    i += 1
            else:
                self.headers.append('治疗信息' + str(treNum))
                i = 0
                for obj_class_name in self.trementInfoTable:
                    obj = obj_class_name()
                    self.headers.extend(obj.get_export_header(self.trementInfoColumns[i], self.buffer))
                    i += 1

        wb = Workbook()
        ws = wb.active
        # ws.alignment = Alignment(horizontal='center', vertical='center')
        ws.title = '导出样本数据'
        ws.append(self.headers)
        '''
        for pid in self.pids:
            for treNum in self.treNums:
                row = []
                i = 0
                for obj_class_name in self.tables:
                    obj = obj_class_name()
                    row.extend(obj.get_export_row(self.columns[i], self.buffer, pid, treNum))
                    i += 1
                ws.append(row)
        '''
        for pid in self.pids:
            row = []
            for treNum in self.treNums:
                if treNum == 0:
                    i = 0
                    for obj_class_name in self.baseLineTable:
                        obj = obj_class_name()
                        row.extend(obj.get_export_row(self.baseLineColumns[i], self.buffer, pid, treNum))
                        i += 1
                else:
                    row.append('')
                    i = 0
                    for obj_class_name in self.trementInfoTable:
                        obj = obj_class_name()
                        row.extend(obj.get_export_row(self.trementInfoColumns[i], self.buffer, pid, treNum))
                        i += 1
            ws.append(row)


        wb.save('test.xlsx')
        content = save_virtual_workbook(wb)
        resp = make_response(content)
        resp.headers["Content-Disposition"] = 'attachment; filename=samples.xlsx'
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp

    def __init_buffer(self):
        for obj_class in self.tables:
            name = obj_class.__name__
            if name == 'Patient':
                obj_array = obj_class.query.filter(obj_class.id.in_(self.pids), obj_class.is_delete == 0).all()
            elif name == 'PastHis':
                obj_array = obj_class.query.filter(obj_class.pid.in_(self.pids), obj_class.is_delete == 0).all()
                drug_history_array = DrugHistory.query.filter(DrugHistory.pid.in_(self.pids),
                                                              DrugHistory.is_delete == 0).all()
            elif name == 'IniDiaPro':
                obj_array = obj_class.query.filter(obj_class.pid.in_(self.pids), obj_class.is_delete == 0).all()
            elif name == 'Surgery' or name == 'OneToFive':
                obj_array = obj_class.query.filter(obj_class.pid.in_(self.pids), obj_class.treNum.in_(self.treNums),
                                                   obj_class.is_delete == 0).all()
                detail_trePlan_array = DetailTrePlan.query.filter(DetailTrePlan.pid.in_(self.pids),
                                                                  obj_class.treNum.in_(self.treNums),
                                                                  DetailTrePlan.is_delete == 0).all()
            else:
                obj_array = obj_class.query.filter(obj_class.pid.in_(self.pids), obj_class.treNum.in_(self.treNums),
                                                   obj_class.is_delete == 0).all()

            if name == 'Patient' or name == 'IniDiaPro':
                self.add_buffer(name, self.classify_by_pid(obj_array))
            elif name == 'PastHis':
                self.add_buffer(name, self.classify_by_pid(obj_array))
                self.add_buffer('DrugHistory', self.array_classify_by_pid(drug_history_array))
            elif (name == 'ImageExams' or
                  name == 'SideEffect' or name == 'Signs'):
                self.add_buffer(name, self.array_classify_by_treNum(obj_array))
            elif name == 'Surgery' or name == 'OneToFive':
                self.add_buffer(name, self.classify_by_treNum(obj_array))
                self.add_buffer('DetailTrePlan', self.array_classify_by_treNum(detail_trePlan_array))
            else:
                self.add_buffer(name, self.classify_by_treNum(obj_array))

    # 缓存数据到内存中, 方便查询
    def add_buffer(self, key, value):
        self.buffer[key] = value

    def classify_by_pid(self, items):
        data = {}
        for item in items:
            if getattr(item, 'pid', None):
                data[item.pid] = item
            else:
                data[item.id] = item
        return data

    def array_classify_by_pid(self, items):
        data = {}
        for item in items:
            pid = getattr(item, 'pid')
            if data.get(pid) is None:
                data[pid] = []
            data[pid].append(item)
        return data

    # pid有多个，需要按照treNum分类。
    def classify_by_treNum(self, items):
        '''
        :param items:[objent]
        :return: map = {
            pid:{
                "total":xxx,
                treNum:obj
            }
        }
        '''
        data = {}
        for item in items:
            pid = getattr(item, 'pid')
            if data.get(pid) is None:
                data[pid] = {}
                data[pid]['total'] = 0
            if data.get(pid).get(item.treNum) is None:
                data[pid][item.treNum] = item
                data[pid]['total'] += 1
        return data

    def array_classify_by_treNum(self, items):
        '''
        :param items:[objent]
        :return: map = {
            pid:{
                "total":xxx,
                treNum:[]
            }
        }
        '''
        data = {}
        for item in items:
            pid = getattr(item, 'pid')
            if data.get(pid) is None:
                data[pid] = {}
                data[pid]['total'] = 0
            if data.get(pid).get(item.treNum) is None:
                data[pid][item.treNum] = []
                data[pid]['total'] += 1
            data[pid][item.treNum].append(item)

        return data
