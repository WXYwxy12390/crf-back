import copy

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime, SmallInteger, and_
from sqlalchemy.orm.attributes import flag_modified

from app.libs.enums import ModuleStatus, GeneValue
from app.models.base import Base, ModificationAndDoubt, db
# 病人基本信息表
from app.models.crf_info import FollInfo
from app.models.cycle import MoleDetec, Immunohis, Signs, SideEffect
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams
from app.models.researchPatient import ResearchPatient
from app.models.therapy_record import PatDia, DetailTrePlan
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy
from app.utils.date import get_birth_date_by_id_card, get_age_by_birth
import numpy as np
from app.libs.enums import BioReason


class Patient(Base, ModificationAndDoubt):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='病人id')
    patNumber = Column(String(255), comment='编号')  # 长度
    _account = Column(String(40), comment='录入人,多个以逗号分隔,格式为(,17,23,)')
    account = Column(JSON, comment='录入人,多个以逗号分隔,格式为(,17,23,)')

    _researchCenter = Column(String(20), comment='研究中心,多个以逗号分隔,格式为(,17,23,)')
    researchCenter = Column(Integer, comment='研究中心,多个以逗号分隔,格式为(,17,23,)')

    idNumber = Column(String(18), comment='身份证号')
    hospitalNumber = Column(String(255), comment='住院号')  # 长度
    patientName = Column(String(100), comment='姓名')
    gender = Column(SmallInteger, comment='性别')  # 格式问题
    _gender = Column(String(2), comment='性别')  # 格式问题
    birthday = Column(Date, comment='出生日期')
    phoneNumber1 = Column(String(20), comment='电话号码1')  # 长度
    phoneNumber2 = Column(String(20), comment='电话号码2')  # 长度
    updateTime = Column(DateTime, comment='更新时间')
    nextFollowupTime = Column(DateTime, comment='随访时间')
    finishFollowup = Column(Integer, comment='是否完成随访(True:1、False:0)')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')
    module_status = Column(JSON, comment='各访视的各模块的状态，0未提交，1未启动监察，2CRA监察中，3CRA有质疑，4有回复，5CRA已完成')
    cycle_is_submit = Column(JSON, comment='记录各访视是否已经提交，0已提交，1未提交')
    # 和导出功能有关
    export_header_map = {'patNumber': '编号', 'researchCenter': '研究中心', 'idNumber': '身份证号', 'patientName': '姓名',
                         'hospitalNumber': '住院号', 'gender': '性别', 'birthday': '出生日期', 'age': '年龄',
                         'phoneNumber1': '电话号码1', 'phoneNumber2': '电话号码2'}

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        # header = []
        header = np.zeros(0, dtype=str)
        for column in columns:
            header = np.append(header, self.export_header_map.get(column))
            # header.append(self.export_header_map.get(column))
        Patient.header_num = len(header)
        return header

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        gender_map = {0: "女", 1: "男", "/": "/"}
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('Patient').get(pid) is None:
            # row.extend(['/']*Patient.header_num)
            row = np.append(row, ['/'] * Patient.header_num)
            return row
        obj = buffer.get('Patient').get(pid)
        for column in columns:
            if column == 'gender':
                value = self.filter_none(obj, column)
                value = gender_map.get(value)
                # row.append(value)
                row = np.append(row, value)
            elif column == 'age':
                idNumber = getattr(obj, 'idNumber')
                age = get_age_by_birth(get_birth_date_by_id_card(idNumber))
                value = age if age else '/'
                # row.append(value)
                row = np.append(row, value)
            elif column == 'researchCenter':
                value = self.filter_none(obj, column)
                if value != '/':
                    value = buffer.get('ResearchCenter').get(value)
                # row.append(value)
                row = np.append(row, value)
            else:
                value = self.filter_none(obj, column)
                # row.append(value)
                row = np.append(row, value)
        return row

    def keys(self):
        return ['id', 'patNumber', 'account', 'researchCenter', 'idNumber', 'hospitalNumber',
                'patientName', 'gender', 'birthday', 'phoneNumber1', 'phoneNumber2', 'updateTime', 'nextFollowupTime',
                'finishFollowup', 'update_time', '_researchCenter', '_account', '_gender',
                'modification', 'doubt', 'module_status', 'cycle_is_submit']

    def get_fotmat_info(self):
        pat_dia = Patient.get_pat_dia([self.id])
        foll_info = FollInfo.query.filter_by(pid=self.id).order_by(FollInfo.date.desc()).first()
        liv_sta_info = None
        if foll_info:
            val = foll_info.livSta
            if val == 1:
                liv_sta_info = '死亡'
            elif val == 2:
                liv_sta_info = '存活'
            elif val == 3:
                liv_sta_info = '失联'
        data = {
            'id': self.id,
            'patNumber': self.patNumber,
            'hospitalNumber': self.hospitalNumber,
            'patientName': self.patientName,
            'idNumber': self.idNumber,
            'phoneNumber': self.phoneNumber1,
            'gender': self.gender,
            'age': get_age_by_birth(get_birth_date_by_id_card(self.idNumber)),
            'patDia': pat_dia[self.id] if pat_dia else None,
            'update_time': self.update_time,
            'create_time': self.create_time,
            'research_center_id': self.researchCenter,
            'livSta': liv_sta_info
        }
        return data

    def delete(self):
        self.is_delete = 1
        self.delete_table(PastHis)
        self.delete_table(DrugHistory)
        self.delete_table(IniDiaPro)
        self.delete_table(SpecimenInfo)
        self.delete_table(FollInfo)

        self.delete_table(BloodRoutine)
        self.delete_table(BloodBio)
        self.delete_table(Thyroid)
        self.delete_table(Coagulation)
        self.delete_table(MyocardialEnzyme)
        self.delete_table(Cytokines)
        self.delete_table(LymSubsets)
        self.delete_table(UrineRoutine)
        self.delete_table(TumorMarker)

        self.delete_table(Lung)
        self.delete_table(OtherExams)
        self.delete_table(ImageExams)

        self.delete_table(Immunohis)
        self.delete_table(MoleDetec)
        self.delete_table(Signs)
        self.delete_table(SideEffect)

        self.delete_table(TreRec)
        self.delete_table(OneToFive)
        self.delete_table(Surgery)
        self.delete_table(Radiotherapy)
        self.delete_table(DetailTrePlan)

        self.delete_table(ResearchPatient)

    # 删除该病人在T模块的数据
    def delete_table(self, T):
        pid = self.id
        records = T.query.filter_by(pid=pid).all()
        with db.auto_commit():
            for record in records:
                record.delete()

    @classmethod
    def search(cls, patients, search_data, page, limit, sort=None):
        pids = [patient.id for patient in patients]
        # 与patient表查询相关的。
        if 'patientName' in search_data or 'patNumber' in search_data \
                or 'idNumber' in search_data or 'hospitalNumber' in search_data or 'gender' in search_data:
            condition = Patient.condition_patient(pids, search_data)
            patients = Patient.query.filter(condition).all()
            pids = [patient.id for patient in patients]
        if 'age1' in search_data and 'age2' in search_data:
            patients = [patient for patient in patients if patient.filter_age(search_data['age1'], search_data['age2'])]
            pids = [patient.id for patient in patients]

        # 过滤pdl1，tmb
        if 'PDL1_1' in search_data and 'PDL1_2' in search_data or 'TMB1' in search_data and 'TMB2' in search_data:
            condition = Patient.condition_moleDetec(pids, search_data)
            items = MoleDetec.query.filter(condition).all()
            pids = [item.pid for item in items]

        # 治疗方式
        if 'therapy_method' in search_data:
            pids = Patient.filter_theapy_method(pids, search_data['therapy_method'])

        # 基因突变位点
        if 'genes' in search_data:
            pids = Patient.filter_genes(pids, search_data['genes'])

        # 吸烟，饮酒，激素
        if 'smoke' in search_data or 'drink' in search_data or 'hormone' in search_data:
            condition = Patient.condition_past_his(pids, search_data)
            past_histories = PastHis.query.filter(condition).all()
            pids = [past_history.pid for past_history in past_histories]

        # 病理分期
        if 'cliStage' in search_data or 'patStage' in search_data:
            condition = Patient.condition_iniDiaPro(pids, search_data)
            items = IniDiaPro.query.filter(condition).all()
            pids = [item.pid for item in items]

        # 病理诊断
        if 'patDia' in search_data:
            pids = Patient.filter_patDia(pids, search_data['patDia'])
        # 转移部位 IniDiaPro
        if 'traSite' in search_data:
            pids = Patient.filter_traSite(pids, search_data['traSite'])
        # 样本类型 SpecimenInfo
        if 'specimenType' in search_data:
            pids = Patient.filter_specimenType(pids, search_data['specimenType'])
        # 研究的id号 Research
        if 'research_id' in search_data:
            pids = Patient.filter_research(pids, search_data['research_id'])

        pids = list(set(pids))
        pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(
            Patient.update_time.desc()).paginate(page=page, per_page=limit)

        if sort == 1:
            # 按患者编号倒序
            pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(
                Patient.patNumber.desc()).paginate(page=page, per_page=limit)
        elif sort == 2:
            # 按患者编号正序
            pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(
                Patient.patNumber.asc()).paginate(page=page, per_page=limit)
        elif sort == 3:
            # 按创建时间倒序排列
            pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(
                Patient.create_time.desc()).paginate(page=page, per_page=limit)
        elif sort == 4:
            # 按创建时间正序排列
            pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(
                Patient.create_time.asc()).paginate(page=page, per_page=limit)

        return pagination.items, pagination.total, pids

    # 获取一组样本中最新的病例诊断
    @classmethod
    def get_pat_dia(cls, pids):
        # 把所有的治疗记录拿到，并按照pid进行分组
        tre_recs = TreRec.query.filter(TreRec.is_delete == 0, TreRec.pid.in_(pids)).all()

        dict = {}

        for tre_rec in tre_recs:
            if dict.get(tre_rec.pid) is None:
                dict[tre_rec.pid] = []
            dict[tre_rec.pid].append(tre_rec)
        data = {}

        oneToFives = OneToFive.query.filter(OneToFive.is_delete == 0, OneToFive.pid.in_(pids)).all()
        surgerys = Surgery.query.filter(Surgery.is_delete == 0, Surgery.pid.in_(pids)).all()
        radiotherapys = Radiotherapy.query.filter(Radiotherapy.is_delete == 0, Radiotherapy.pid.in_(pids)).all()
        iniDiapros = IniDiaPro.query.filter(IniDiaPro.is_delete == 0, IniDiaPro.pid.in_(pids)).all()

        oneToFive_map = Patient.getMap(oneToFives)
        surgery_map = Patient.getMap(surgerys)
        radiotherapy_map = Patient.getMap(radiotherapys)

        iniDiapro_map = {}
        for item in iniDiapros:
            pid = item.pid
            if item and item.patDia and item.patDia.get('radio') != []:
                iniDiapro_map[pid] = item.patDia

        for pid, tre_recs in dict.items():
            tre_recs = sorted(tre_recs, key=lambda tre_rec: tre_rec.treNum, reverse=True)
            for tre_rec in tre_recs:
                trement = tre_rec.trement
                treNum = tre_rec.treNum

                if trement is None:
                    continue
                if trement in ['one', 'two', 'three', 'four', 'five', 'other']:
                    if oneToFive_map.get(pid) is None or oneToFive_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = oneToFive_map.get(pid).get(treNum)
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
                elif trement == 'surgery':
                    if surgery_map.get(pid) is None or surgery_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = surgery_map[pid][tre_rec.treNum]
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
                elif trement == 'radiotherapy':
                    if radiotherapy_map.get(pid) is None or radiotherapy_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = radiotherapy_map[pid][tre_rec.treNum]
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
        for pid, item in iniDiapro_map.items():
            if pid not in data:
                data[pid] = iniDiapro_map.get(pid)
        return data if data != {} else None

    @classmethod
    def getMap(cls, model_items):
        dict = {}
        for model_item in model_items:
            pid = model_item.pid
            if dict.get(pid) is None:
                dict[pid] = {}
            dict[pid][model_item.treNum] = model_item
        return dict

    @staticmethod
    def condition_patient(pids, data):

        # 这里必须用and_连起来两个条件，否则会被当作元组
        condtion = and_(Patient.is_delete == 0, Patient.id.in_(pids))
        if 'patientName' in data:
            condtion = and_(condtion, Patient.patientName.like('%' + data['patientName'] + '%'))
        if 'patNumber' in data:
            condtion = and_(condtion, Patient.patNumber.like(data['patNumber'] + '%'))
        if 'idNumber' in data:
            condtion = and_(condtion, Patient.idNumber.like(data['idNumber'] + '%'))
        if 'hospitalNumber' in data:
            condtion = and_(condtion, Patient.hospitalNumber.like(data['hospitalNumber'] + '%'))
        if 'gender' in data:
            condtion = and_(condtion, Patient.gender == data['gender'])

        return condtion

    @staticmethod
    def condition_past_his(pids, data):

        condtion = and_(PastHis.is_delete == 0, PastHis.pid.in_(pids))
        if 'smoke' in data:
            condtion = and_(condtion, PastHis.smoke == data['smoke'])
        if 'drink' in data:
            condtion = and_(condtion, PastHis.drink == data['drink'])
        if 'hormone' in data:
            condtion = and_(condtion, PastHis.hormone == data['hormone'])
        return condtion

    @staticmethod
    def condition_iniDiaPro(pids, data):

        condtion = and_(IniDiaPro.is_delete == 0, IniDiaPro.pid.in_(pids))
        if 'patStage' in data:
            condtion = and_(condtion, IniDiaPro.patStage == data['patStage'])
        if 'cliStage' in data:
            condtion = and_(condtion, IniDiaPro.cliStage == data['cliStage'])
        return condtion

    @staticmethod
    def condition_moleDetec(pids, search_data):
        condtion = and_(MoleDetec.is_delete == 0, MoleDetec.pid.in_(pids))
        if 'PDL1_1' in search_data and 'PDL1_2' in search_data:
            condtion = and_(condtion, MoleDetec.PDL1 >= search_data['PDL1_1'], MoleDetec.PDL1 <= search_data['PDL1_2'])
        if 'TMB1' in search_data and 'TMB2' in search_data:
            condtion = and_(condtion, MoleDetec.TMB >= search_data['TMB1'], MoleDetec.TMB <= search_data['TMB2'])

        return condtion

    # 过滤基因突变
    @classmethod
    def filter_genes(cls, pids, genes):
        mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.pid.in_(pids)).all()
        mole_detec_map = {}
        for mole_detec in mole_detecs:
            pid = mole_detec.pid
            if mole_detec_map.get(pid) is None:
                mole_detec_map[pid] = []
            mole_detec_map[pid].append(mole_detec)

        res = []
        for pid, mole_detecs in mole_detec_map.items():
            yang_record = set()
            yin_record = set()
            unknown_record = set()
            for mole_detec in mole_detecs:
                if mole_detec.ALK == GeneValue.Yang.value:
                    yang_record.add('ALK')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('ALK')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('ALK')

                if mole_detec.BIM == GeneValue.Yang.value:
                    yang_record.add('BIM')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('BIM')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('BIM')

                if mole_detec.BRAF == GeneValue.Yang.value:
                    yang_record.add('BRAF')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('BRAF')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('BRAF')

                if mole_detec.cMET == GeneValue.Yang.value:
                    yang_record.add('cMET')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('cMET')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('cMET')

                if mole_detec.EGFR == GeneValue.Yang.value:
                    yang_record.add('EGFR')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('EGFR')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('EGFR')

                if mole_detec.HER_2 == GeneValue.Yang.value:
                    yang_record.add('HER_2')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('HER_2')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('HER_2')

                if mole_detec.KRAS == GeneValue.Yang.value:
                    yang_record.add('KRAS')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('KRAS')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('KRAS')

                if mole_detec.PIK3CA == GeneValue.Yang.value:
                    yang_record.add('PIK3CA')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('PIK3CA')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('PIK3CA')

                if mole_detec.ROS1 == GeneValue.Yang.value:
                    yang_record.add('ROS1')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('ROS1')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('ROS1')

                if mole_detec.RET == GeneValue.Yang.value:
                    yang_record.add('RET')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('RET')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('RET')

                if mole_detec.UGT1A1 == GeneValue.Yang.value:
                    yang_record.add('UGT1A1')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('UGT1A1')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('UGT1A1')

                if mole_detec.UGT1A1 == GeneValue.Yang.value:
                    yang_record.add('NTRK')
                elif mole_detec.ALK == GeneValue.Yin.value:
                    yin_record.add('NTRK')
                elif mole_detec.ALK == GeneValue.Unknown.value:
                    unknown_record.add('NTRK')

            # 去重
            yang_record = list(yang_record)
            yin_record = list(yin_record)
            unknown_record = list(unknown_record)
            flag = True
            for gene in genes:
                name = gene['gene']
                value = gene['value']
                if (value == GeneValue.Yang.value) and (name not in yang_record):
                    flag = False
                    break
                if (value == GeneValue.Yin.value) and (name not in yin_record):
                    flag = False
                    break
                if (value == GeneValue.Unknown.value) and (name not in unknown_record):
                    flag = False
                    break
            if flag:
                res.append(pid)
        return res

    def filter_age(self, age1, age2):
        if self.idNumber is None or self.idNumber == "":
            return None
        birth = get_birth_date_by_id_card(self.idNumber)
        age = get_age_by_birth(birth)
        if age is None or age < age1 or age > age2:
            return None
        return self

    # @classmethod
    # def filter_PDL(cls,pids,PDL_val1,PDL_val2):
    #     mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete==0,MoleDetec.pid.in_(pids),
    #                                          MoleDetec.PDL1 >= PDL_val1,MoleDetec.PDL1 <= PDL_val2).all()
    #     data = [mole_detec.pid for mole_detec in mole_detecs]
    #     return data
    # @classmethod
    # def filter_TMB(cls,pids,TMB1,TMB2):
    #     mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.pid.in_(pids),
    #                                          MoleDetec.TMB >= TMB1, MoleDetec.TMB <= TMB2).all()
    #     data = [mole_detec.pid for mole_detec in mole_detecs]
    #     return data

    @classmethod
    def filter_theapy_method(cls, pids, method):
        trement = method.get('trement')
        treSolu = method.get('treSolu')

        if trement:
            tre_recs = TreRec.query.filter(TreRec.is_delete == 0, TreRec.pid.in_(pids), TreRec.trement == trement).all()
            pids = [tre_rec.pid for tre_rec in tre_recs]
        if treSolu is None:
            return pids

        # 只有1-5线，和其他，中有详细治疗。
        items = OneToFive.query.filter(OneToFive.is_delete == 0, OneToFive.pid.in_(pids)).all()
        tre_rec_map = {}
        for item in items:
            if item.treSolu is None:
                continue
            pid = item.pid
            if tre_rec_map.get(pid) is None:
                tre_rec_map[pid] = []
            tre_rec_map[pid].extend(item.treSolu.split(','))
        res = []
        for pid, treSolus in tre_rec_map.items():
            if treSolu in treSolus:
                res.append(pid)

        return list(set(res))

    @classmethod
    def filter_patDia(cls, pids, items):

        pat_dia = Patient.get_pat_dia(pids)
        data = []
        for pid, pat_dia in pat_dia.items():
            flag = True
            radio = pat_dia.get('radio')
            if radio is None or radio == []:
                continue
            for item in items:
                is_start = False
                for radio_item in radio:
                    if radio_item.startswith(item):
                        is_start = True
                if is_start == False:
                    flag = False
                    break
            if flag:
                data.append(pid)
        return data

    @classmethod
    def filter_traSite(cls, pids, items):
        ini_dia_pros = IniDiaPro.query.filter(IniDiaPro.pid.in_(pids)).all()
        patient_ids = []
        for ini_dia_pro in ini_dia_pros:
            if ini_dia_pro.traSite is None:
                continue
            radio = ini_dia_pro.traSite.get('radio')
            flag = True
            for item in items:
                if item not in radio:
                    flag = False
                    break
            if flag:
                patient_ids.append(ini_dia_pro.pid)

        return patient_ids

    @classmethod
    def filter_specimenType(cls, pids, type):
        specimenInfo_array = SpecimenInfo.query.filter(SpecimenInfo.pid.in_(pids),
                                                       SpecimenInfo.is_delete == 0).all()
        specimenInfo_classify_by_pid = cls.array_classify_by_pid(specimenInfo_array)
        patient_ids = []
        for key, value in specimenInfo_classify_by_pid.items():
            flag = False
            for specimentInfo in value:
                if specimentInfo.type and specimentInfo.type['radio'][0] == type:
                    flag = True
                    break
            if flag:
                patient_ids.append(key)
        return patient_ids

    @classmethod
    def filter_research(cls, pids, rid):
        research_patient_list = ResearchPatient.query.filter(ResearchPatient.is_delete == 0,
                                                             ResearchPatient.rid == rid,
                                                             ResearchPatient.pid.in_(pids)).all()
        patient_ids = [research_patient.pid for research_patient in research_patient_list]
        return patient_ids


    @classmethod
    def array_classify_by_pid(cls, items):
        data = {}
        for item in items:
            pid = getattr(item, 'pid')
            if data.get(pid) is None:
                data[pid] = []
            data[pid].append(item)
        return data

    def submit_module(self, module, treNum):
        flag = True  # 标记是否成功提交
        treNum = str(treNum)
        temp = copy.copy(self.module_status)
        if temp is None:
            temp = {}
        if temp.get(module) is None:
            temp[module] = {}
        status = temp[module].get(treNum)
        if status is None or status == ModuleStatus.UnSubmitted.value:
            temp[module][treNum] = ModuleStatus.UnInitiateMonitoring.value
            with db.auto_commit():
                self.module_status = copy.copy(temp)
                flag_modified(self, 'module_status')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        else:
            flag = False
        return flag

    def start_monitor(self, module, treNum):
        treNum_str = str(treNum)
        flag = False  # 标志是否成功启动监察
        if not self.cycle_is_submit:
            return flag
        if not self.cycle_is_submit.get(treNum_str):
            return flag
        if not self.module_status or not self.module_status.get(module) or not self.module_status[module].get(
                treNum_str):
            return flag
        if self.module_status[module][treNum_str] != ModuleStatus.UnInitiateMonitoring.value:
            return flag
        temp = copy.copy(self.module_status)
        temp[module][treNum_str] = ModuleStatus.CRAMonitoring.value
        flag = True
        with db.auto_commit():
            self.module_status = temp
            flag_modified(self, 'module_status')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag

    def finish(self, module, treNum):
        treNum_str = str(treNum)
        flag = False  # 标志是否成功完成模块
        if not self.module_status or not self.module_status.get(module) or not self.module_status[module].get(
                treNum_str):
            return flag
        if self.module_status[module][treNum_str] not in [ModuleStatus.CRAMonitoring.value, ModuleStatus.CRADoubt.value,
                                                          ModuleStatus.WithReply.value]:
            return flag
        temp = copy.copy(self.module_status)
        temp[module][treNum_str] = ModuleStatus.CRAFinish.value
        flag = True
        with db.auto_commit():
            self.module_status = temp
            flag_modified(self, 'module_status')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag


# 病人既往史表
class PastHis(Base, ModificationAndDoubt):
    __tablename__ = 'pastHis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')

    basDisHis = Column(JSON, comment='基础疾病史,多个以逗号分隔')
    _basDisHis = Column(String(100), comment='基础疾病史,多个以逗号分隔')  # 长度

    infDisHis = Column(JSON, comment='传染疾病史,多个以逗号分隔')
    _infDisHis = Column(String(100), comment='传染疾病史,多个以逗号分隔')  # 长度

    tumor = Column(Boolean, comment='肿瘤史（无、有）')

    tumHis = Column(JSON, comment='肿瘤史,多个以逗号分隔')  # 长度
    _tumHis = Column(String(100), comment='肿瘤史,多个以逗号分隔')  # 长度

    tumorFam = Column(Boolean, comment='肿瘤家族史（无、有）')

    tumFamHis = Column(JSON, comment='肿瘤家族史,多个以逗号分隔')
    _tumFamHis = Column(String(100), comment='肿瘤家族史,多个以逗号分隔')  # 长度

    smoke = Column(Boolean, comment='是否吸烟')
    smokingHis = Column(JSON,
                        comment='吸烟史, {stopSmoke: 是否戒烟, smokeDayAvg: 日平均吸烟量/支, smokeYearAvg: 累计吸烟时间/年,stopSmokeHis: 戒烟时间}')
    drink = Column(Boolean, comment='是否饮酒（否、是）')
    drinkingHis = Column(JSON,
                         comment='饮酒史, {stopDrink: 是否戒酒, drinkDayAvg: 日平均饮酒量, drinkYearAvg: 累计饮酒时间/年,stopDrinkHis: 戒酒时间}')
    hormone = Column(Boolean, comment='是否长期使用激素')
    hormoneUseHis = Column(JSON,
                           comment='激素使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')
    drug = Column(Boolean, comment='是否长期使用药物')
    drugUseHis = Column(JSON,
                        comment='药物使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'basDisHis': '基础疾病史', 'infDisHis': '传染病史', 'tumor': '是否有肿瘤史', 'tumHis': '肿瘤史',
                         'tumorFam': '是否有肿瘤家族史', 'tumFamHis': '肿瘤家族史', 'smoke': '是否吸烟', 'smokingHis': '吸烟史',
                         'drink': '是否饮酒', 'drinkingHis': '饮酒史',
                         'hormone': '是否长期使用激素', 'hormoneUseHis': '激素使用史', 'drug': '是否长期使用药物', 'drugUseHis': '药物使用史'}

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        # row = []
        row = np.zeros(0, dtype=str)
        if buffer.get('PastHis').get(pid) is None:
            # row.extend(['/']*PastHis.header_num)
            row = np.append(row, ['/'] * PastHis.header_num)
            return row
        obj = buffer.get('PastHis').get(pid)

        for column in columns:
            x = getattr(obj, column)

            if column == 'basDisHis' or column == 'infDisHis':
                value = self.format_radio_data(obj, column)
                # row.append(value)
                row = np.append(row, value)
            elif column == 'tumHis':
                if_tum = getattr(obj, 'tumor')
                if if_tum:
                    value = self.format_radio_data(obj, column)
                    # row.append(value)
                    row = np.append(row, value)
                else:
                    # row.append('/')
                    row = np.append(row, '/')
            elif column == 'tumFamHis':
                if_tumorFam = getattr(obj, 'tumorFam')
                if if_tumorFam:
                    value = self.format_radio_data(obj, column)
                    # row.append(value)
                    row = np.append(row, value)
                else:
                    # row.append('/')
                    row = np.append(row, '/')
            elif column == 'drinkingHis':
                value = self.format_drink_history(obj)
                # row.append(value)
                row = np.append(row, value)
            elif column == 'smokingHis':
                value = self.format_smoke_history(obj)
                # row.append(value)
                row = np.append(row, value)
            elif column == 'hormoneUseHis':
                if_hormone = getattr(obj, 'hormone')
                if (if_hormone and buffer.get('DrugHistory') is not None and
                        buffer.get('DrugHistory').get(pid) is not None):
                    value = ''
                    for drug_history_obj in buffer.get('DrugHistory').get(pid):
                        if drug_history_obj.type == 1:
                            value += self.filter_none(drug_history_obj.drug_name) + ','
                            value += self.filter_none(drug_history_obj.drug_dose) + ','
                            value += str(self.filter_none(drug_history_obj.use_time)) + '月;'
                else:
                    value = '/'
                # row.append(value)
                row = np.append(row, value)

            elif column == 'drugUseHis':
                if_drug = getattr(obj, 'drug')
                if (if_drug and buffer.get('DrugHistory') is not None and
                        buffer.get('DrugHistory').get(pid) is not None):
                    value = ''
                    for drug_history_obj in buffer.get('DrugHistory').get(pid):
                        if drug_history_obj.type == 0:
                            value += self.filter_none(drug_history_obj.drug_name) + ','
                            value += self.filter_none(drug_history_obj.drug_dose) + ','
                            value += str(self.filter_none(drug_history_obj.use_time)) + '月;'
                else:
                    value = '/'
                # row.append(value)
                row = np.append(row, value)
            elif type(x) == bool:
                value = self.filter_none(self.change_bool_to_yes_or_no(x))
                # row.append(value)
                row = np.append(row, value)
            else:
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
        PastHis.header_num = len(header)
        return header

    def keys(self):
        return ['id', 'pid', 'basDisHis', 'infDisHis', 'tumor', 'tumHis', 'tumorFam', 'tumFamHis', 'smoke',
                'smokingHis', 'drink', 'drinkingHis', 'hormone', 'drug', '_basDisHis', '_tumHis',
                '_tumFamHis', 'modification', 'doubt']

    # 和导出功能有关
    def format_drink_history(self, object):
        if object is None:
            return '/'
        is_drink = object.drink
        info = object.drinkingHis
        value = '/'
        if is_drink == 1:
            value = '累积饮酒时间（年）' + str(info.get('drinkYearAvg')) + '日平均饮酒量（mL）' + str(info.get('drinkDayAvg'))
            if_quit_drink = info.get('stopDrink')
            if if_quit_drink:
                value += '，已戒酒'
                quit_drink_time = info.get('stopDrinkHis')
                value += '，戒酒时间' + str(quit_drink_time)
            else:
                value += ',未戒酒'
        elif is_drink == 0:
            value = '无'
        return value

    # 和导出功能有关
    def format_smoke_history(self, object):
        if object is None:
            return '/'
        is_smoke = object.smoke
        info = object.smokingHis
        value = '/'
        if is_smoke == 1:
            value = '累积吸烟时间（年）' + str(info.get('smokeYearAvg')) + '日平均吸烟量（支）' + str(info.get('smokeDayAvg'))
            if_quit_smoke = info.get('stopSmoke')
            if if_quit_smoke:
                value += '，已戒烟'
                quit_smoke_time = info.get('stopSmokeHis')
                value += '，戒烟时间' + str(quit_smoke_time)
            else:
                value += ',未烟酒'
        elif is_smoke == 0:
            value = '无'
        return value


# 激素史与药物史
class DrugHistory(Base, ModificationAndDoubt):
    __tablename__ = 'drug_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    type = Column(SmallInteger, comment='type=1,激素史，type = 0，其他药物史')
    drug_name = Column(String(255), comment='药物名称')
    drug_dose = Column(String(255), comment='日使用剂量')
    use_time = Column(Float, comment='累积使用时间（月）')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    export_header_map = {'drug_name': '药物名称', 'drug_dose': '日使用剂量', 'use_time': '累积使用时间（月）'}

    def keys(self):
        return ['id', 'drug_name', 'drug_dose', 'use_time', 'modification', 'doubt']


# 病人初诊过程信息表
class IniDiaPro(Base, PatDia, ModificationAndDoubt):
    __tablename__ = 'iniDiaPro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id', index=True)
    PSScore = Column(Integer, comment='首诊PS评分0-4')

    cliniManifest = Column(JSON, comment='临床表现,多个以逗号分隔')  # 长度
    _cliniManifest = Column(String(40), comment='临床表现,多个以逗号分隔')  # 长度

    videography = Column(Boolean, comment='影像学 0-周围型；1-中央型')

    part = Column(JSON, comment='部位,多个以逗号分隔')
    _part = Column(String(100), comment='部位,多个以逗号分隔')

    bioMet = Column(JSON, comment='活检方式,多个以逗号分隔')  # 长度
    _bioMet = Column(String(40), comment='活检方式,多个以逗号分隔')  # 长度

    pleInv = Column(Boolean, comment='是否胸膜侵犯')
    speSite = Column(String(255), comment='标本部位')
    firVisDate = Column(Date, comment='初诊日期')
    patReDate = Column(Date, comment='病理报告日期')
    patNum = Column(String(255), comment='病理号')  # 改为字符串

    patDia = Column(JSON, comment='病理诊断,多个以逗号分隔')
    _patDia = Column(String(10000), comment='病理诊断,多个以逗号分隔')
    _patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')

    cliniDia = Column(JSON, comment='临床诊断')

    mitIma = Column(String(255), comment='核分裂像')
    comCar = Column(String(255), comment='复合性癌')  # 长度
    necArea = Column(Float, comment='坏死面积')
    massSize = Column(String(255), comment='肿块大小')
    Ki67 = Column(Float, comment='Ki67')

    traSite = Column(JSON, comment='转移部位')  # 长度
    _traSite = Column(String(100), comment='转移部位')  # 长度

    TSize = Column(String(255), comment='TSize')  # 文本
    stage = Column(String(30), comment='分期情况')  # 格式问题
    cStage = Column(JSON, comment='c分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    cliStage = Column(String(30), comment='临床分期')
    pStage = Column(JSON, comment='p分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    patStage = Column(String(30), comment='病理分期')
    cRemark = Column(Text(10000), comment='c备注')
    pRemark = Column(Text(10000), comment='p备注')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'PSScore': 'PS评分', 'cliniManifest': '临床表现', 'videography': '影像学', 'part': '部位',
                         'bioMet': '活检方式', 'pleInv': '是否胸膜侵犯',
                         'speSite': '标本部位', 'firVisDate': '初诊日期', 'patReDate': '病理报告日期', 'patNum': '病理号',
                         'patDia': '病理诊断', 'mitIma': '核分裂像', 'cliniDia': '临床诊断',
                         'comCar': '复合性癌', 'necArea': '坏死面积', 'massSize': '肿块大小', 'traSite': '转移部位',
                         'TSize': 'TSize', 'stage': '分期情况',
                         'cStage': 'C分期(T,N,M)', 'pStage': 'P分期(T,N,M)', 'cliStage': '临床分期', 'patStage': '病理分期',
                         'cRemark': 'C备注', 'pRemark': 'P备注'}

    def keys(self):
        return ["id", "PSScore", "cliniManifest", "videography", "part", "bioMet", "pleInv", "speSite", "firVisDate",
                "patReDate", "patNum", "patDia", "mitIma", "comCar", "necArea", "massSize", "Ki67",
                "traSite", "TSize", "stage", "cStage", "cliStage", "pStage", "patStage", 'cRemark', 'pRemark',
                '_cliniManifest', '_part', '_bioMet', '_traSite', '_patDia', '_patDiaOthers', 'cliniDia',
                'modification', 'doubt']

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = np.zeros(0, dtype=str)
        for column in columns:
            if column == 'cliniDia':
                header = np.append(header, ['临床诊断', '临床诊断:肺癌', '临床诊断:食道癌', '临床诊断:乳腺癌',
                                            '临床诊断:胸腺癌', '临床诊断:消化系统肿瘤', '临床诊断:头颈部肿瘤', '临床诊断:血液系统肿瘤',
                                            '临床诊断:泌尿生殖系统肿瘤', '临床诊断:骨肿瘤', '临床诊断:软组织肉瘤', '临床诊断:其他'])
            else:
                header = np.append(header, self.export_header_map.get(column))
        IniDiaPro.header_num = len(header)
        return header

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        videography_map = {0: '周围型', 1: '中央型', "/": "/"}
        stage_map = {'1': '未住院', '2': 'C/P/S均无法分期', '3': '仅C分期',
                     '4': '仅P分期', '5': 'C分期和P分期', "/": "/"}

        row = np.zeros(0, dtype=str)
        if buffer.get('IniDiaPro').get(pid) is None:
            row = np.append(row, ['/'] * IniDiaPro.header_num)
            return row
        obj = buffer.get('IniDiaPro').get(pid)
        for column in columns:
            x = getattr(obj, column)
            if column == 'videography':
                value = self.filter_none(obj, column)
                value = videography_map.get(value)
                row = np.append(row, value)
            elif column == 'stage':
                value = self.filter_none(obj, column)
                value = stage_map.get(value)
                row = np.append(row, value)
            elif (column == 'cliniManifest' or column == 'part' or
                  column == 'bioMet' or column == 'traSite'):
                value = self.format_radio_data(obj, column)
                row = np.append(row, value)
            elif column == 'patDia':
                value = self.format_patDia(obj)
                row = np.append(row, value)
            elif column == 'cliniDia':
                value = self.format_cliniDia(obj)
                row = np.append(row, value)
            elif column == 'cStage':
                stage_value = self.filter_none(obj, 'stage')
                value = self.format_TNM(x) if stage_value in ['3', '5'] else '/'
                row = np.append(row, value)
            elif column == 'cliStage' or column == 'cRemark':
                stage_value = self.filter_none(obj, 'stage')
                value = self.filter_none(obj, column) if stage_value in ['3', '5'] else '/'
                row = np.append(row, value)
            elif column == 'patStage' or column == 'pRemark':
                stage_value = self.filter_none(obj, 'stage')
                value = self.filter_none(obj, column) if stage_value in ['4', '5'] else '/'
                row = np.append(row, value)
            elif column == 'pStage':
                stage_value = self.filter_none(obj, 'stage')
                value = self.format_TNM(x) if stage_value in ['4', '5'] else '/'
                row = np.append(row, value)
            elif type(x) == bool:
                value = self.filter_none(self.change_bool_to_yes_or_no(x))
                row = np.append(row, value)
            else:
                value = self.filter_none(obj, column)
                row = np.append(row, value)
        return row

    def format_TNM(self, stage):
        if not stage:
            return '/'
        stage_str = str(stage)
        split_list = stage_str.split(',')
        split_list[0] = 'T' + split_list[0]
        split_list[1] = 'N' + split_list[1]
        split_list[2] = 'M' + split_list[2]
        value = split_list[0] + split_list[1] + split_list[2]
        return value

    def format_cliniDia(self, obj):
        cliniDia_map = {'lung_can': '肺癌', 'eso_can': '食道癌', 'bre_can': '乳腺癌', 'thy_can': '胸腺癌',
                        'dig_tum': '消化系统肿瘤', 'head_neck_tum': '头颈部肿瘤', 'blo_tum': '血液系统肿瘤',
                        'gen_tum': '泌尿生殖系统肿瘤', 'bone_tum': '骨肿瘤', 'soft_tis_sar': '软组织肉瘤',
                        'other': '其他'}
        cliniDia_key = ['lung_can', 'eso_can', 'bre_can', 'thy_can', 'dig_tum', 'head_neck_tum',
                        'blo_tum', 'gen_tum', 'bone_tum', 'soft_tis_sar', 'other']

        dic_value = obj.cliniDia

        if not dic_value:
            return ['/'] * 12

        dic_value_keys = dic_value.keys()
        array_value = ['']
        for key in cliniDia_key:
            if key in dic_value_keys:
                array_value[0] += cliniDia_map.get(key) + ' '
                array_value.append(self.filter_none(dic_value.get(key)))
            else:
                array_value.append('/')
        return array_value


class SpecimenInfo(Base, ModificationAndDoubt):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id', index=True)
    number = Column(Text, comment="样本编号")
    type = Column(JSON, comment="样本类型")
    amount = Column(Text, comment="样本数量")
    samplingTime = Column(Date, comment='取样时间')
    storeSite = Column(Text, comment="存储位置")
    bioReason = Column(JSON, comment="活检原因")
    note = Column(Text)

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    doubt = Column(JSON, comment='质疑和回复')

    # 和导出功能有关
    export_header_map = {'number': '样本编号', 'type': '样本类型', 'amount': '样本数量',
                         'samplingTime': '取样时间', 'storeSite': '样本储存位置', 'bioReason': '活检原因',
                         'note': '备注'}

    # 和导出功能有关，得到导出的表的中文抬头
    def get_export_header(self, columns, buffer):
        header = np.zeros(0, dtype=str)
        # 求最多有多少条
        max_num = 0
        for value in buffer.get('SpecimenInfo').values():
            num = len(value)
            if num > max_num:
                max_num = num

        if max_num > 1:
            header_num = max_num
        else:
            header_num = 1

        for i in range(1, header_num + 1):
            for column in columns:
                header = np.append(header, self.export_header_map.get(column) + str(i))
        SpecimenInfo.header_num = len(header)
        return header

    # 和导出功能有关
    def get_export_row(self, columns, buffer, pid, treIndex):
        row = np.zeros(0, dtype=str)
        if buffer.get('SpecimenInfo').get(pid) is None:
            row = np.append(row, ['/'] * SpecimenInfo.header_num)
            return row
        obj_array = buffer.get('SpecimenInfo').get(pid)

        for obj in obj_array:
            for column in columns:
                if column == 'type':
                    value = self.format_type(obj)
                    row = np.append(row, value)
                elif column == 'bioReason':
                    value = self.format_bioReason(obj)
                    row = np.append(row, value)
                else:
                    value = self.filter_none(obj, column)
                    row = np.append(row, value)
        row = np.append(row, ['/'] * (SpecimenInfo.header_num - len(row)))
        return row

    def format_type(self, obj):
        type_dict = getattr(obj, 'type')
        value = '/'
        if not type_dict:
            return value
        radio_dict = type_dict['radio'][0]
        radio = None
        if radio_dict:
            radio = radio_dict[0]
            for i in range(1, len(radio_dict)):
                radio += '-' + radio_dict[i]


        other = type_dict.get('other')
        if radio:
            value = radio
            if other:
                value += ':' + other
        return value

    def format_bioReason(self, obj):
        bioReason_map = {BioReason.IniDiag.value:'初诊诊断', BioReason.Relapse.value:'复发',
                         BioReason.TargetedDrugResis.value:'靶向耐药', BioReason.ImmuneResis.value:'免疫耐药',
                         BioReason.SpeCliSig.value:'特殊临床意义', BioReason.Other.value:'其他'}
        type_dict = getattr(obj, 'bioReason')
        if not type_dict:
            return '/'
        value = '/'
        radio = bioReason_map.get(type_dict['radio'])
        other = type_dict.get('other')
        if radio:
            value = radio
            if other:
                value += ':' + other
        return value

    def keys(self):
        return ['id', 'number', 'type', 'amount', 'samplingTime', 'note', 'storeSite', 'bioReason',
                'modification', 'doubt']
