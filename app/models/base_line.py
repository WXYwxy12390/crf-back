from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime, SmallInteger, and_

from app.models.base import Base
# 病人基本信息表
from app.models.cycle import MoleDetec
from app.models.therapy_record import TreRec, OneToFive
from app.utils.date import get_birth_date_by_id_card, get_age_by_birth, str2date


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='病人id')
    patNumber = Column(String(20), comment='编号')
    account = Column(String(40), comment='录入人,多个以逗号分隔,格式为(,17,23,)')
    researchCenter = Column(String(20), comment='研究中心,多个以逗号分隔,格式为(,17,23,)')
    idNumber = Column(String(18), comment='身份证号', unique=True)
    hospitalNumber = Column(String(20), comment='住院号')
    patientName = Column(String(100), comment='姓名')
    gender = Column(SmallInteger, comment='性别')      #格式问题
    birthday = Column(Date, comment='出生日期')
    phoneNumber1 = Column(String(20), comment='电话号码1')
    phoneNumber2 = Column(String(20), comment='电话号码2')
    updateTime = Column(DateTime, comment='更新时间')
    nextFollowupTime = Column(DateTime, comment='随访时间')
    finishFollowup = Column(Integer, comment='是否完成随访(True:1、False:0)')

    def keys(self):
        return ['id','patNumber','account','researchCenter','idNumber','hospitalNumber',
                    'patientName','gender','birthday','phoneNumber1','phoneNumber2','updateTime','nextFollowupTime','finishFollowup','update_time']

    def get_fotmat_info(self):
        ini_dia_pro = IniDiaPro.query.filter_by(pid=self.id).first()
        data = {
            'id':self.id,
            'patNumber':self.patNumber,
            'hospitalNumber':self.hospitalNumber,
            'patientName':self.patientName,
            'idNumber':self.idNumber,
            'phoneNumber':self.phoneNumber1,
            'gender':self.gender,
            'age':get_age_by_birth(get_birth_date_by_id_card(self.idNumber)),
            'patDia':ini_dia_pro.patDia if ini_dia_pro else None,
            'update_time':self.update_time
        }
        return data

    @classmethod
    def search(cls,patients,search_data):
        if 'patDia' in search_data:
            patients = [patient for patient in patients if patient.filter_patDia(search_data['patDia'])]
        if 'traSite' in search_data:
            patients = [patient for patient in patients if patient.filter_traSite(search_data['traSite'])]
        #病理诊断，病理分期，转移部位
        if 'patStage' in search_data:
            condition = Patient.condition_iniDiaPro(patients, search_data)
            items = IniDiaPro.query.filter(condition).all()
            pids = [item.pid for item in items]
            patients = Patient.query.filter(Patient.id.in_(pids)).all()
        #基因突变位点
        if 'genes' in search_data:
            patients = [patient for patient in patients if patient.filter_genes(search_data['genes'])]
        if 'patientName' in search_data or 'patNumber' in search_data \
                or 'idNumber' in search_data or 'hospitalNumber' in search_data or 'gender' in search_data:
            condition = Patient.condition_patient(patients,search_data)
            patients = Patient.query.filter(condition).all()
        #吸烟，饮酒，激素
        if 'smoke' in search_data or 'drink' in search_data or 'hormone' in search_data:
            condition = Patient.condition_past_his(patients, search_data)
            past_histories = PastHis.query.filter(condition).all()
            pids = [past_history.pid for past_history in past_histories]
            patients = Patient.query.filter(Patient.id.in_(pids)).all()
        if 'age1' in search_data and 'age2' in search_data:
            patients = [patient for patient in patients if patient.filter_age(search_data['age1'],search_data['age2'])]

        if 'PDL1' in search_data and 'PDL2' in search_data:
            patients = [patient for patient in patients if patient.filter_PDL(search_data['PDL1'],search_data['PDL2'])]

        if 'TMB1' in search_data and 'TMB2' in search_data:
            patients = [patient for patient in patients if patient.filter_TMB(search_data['TMB1'],search_data['TMB2'])]

        #治疗方式
        if 'therapy_method' in search_data:
            patients = [patient for patient in patients if patient.filter_theapy_method(search_data['therapy_method'])]


        return patients


    @staticmethod
    def condition_patient(patients, data):
        pids = [patient.id for patient in patients]
        # 这里必须用and_连起来两个条件，否则会被当作元组
        condtion = and_( Patient.id.in_(pids))
        if 'patientName' in data:
            condtion = and_(condtion, Patient.patientName.like('%' + data['patientName'] + '%'))
        if 'patNumber' in data:
            condtion = and_(condtion, Patient.patNumber.like(data['patNumber'] + '%'))
        if 'idNumber' in data:
            condtion = and_(condtion,Patient.idNumber.like(data['idNumber'] + '%'))
        if 'hospitalNumber' in data:
            condtion = and_(condtion,Patient.hospitalNumber.like(data['hospitalNumber'] + '%'))
        if 'gender' in data:
            condtion = and_(condtion, Patient.gender == data['gender'])

        return condtion

    @staticmethod
    def condition_past_his(patients,data):
        pids = [patient.id for patient in patients]
        condtion = and_(PastHis.pid.in_(pids))
        if 'smoke' in data:
            condtion = and_(condtion, PastHis.smoke == data['smoke'])
        if 'drink' in data:
            condtion = and_(condtion, PastHis.drink == data['drink'])
        if 'hormone' in data:
            condtion = and_(condtion, PastHis.hormone == data['hormone'])
        return condtion

    @staticmethod
    def condition_iniDiaPro(patients,data):
        pids = [patient.id for patient in patients]
        condtion = and_(IniDiaPro.pid.in_(pids))
        if 'patStage' in data:
            condtion = and_(condtion, IniDiaPro.patStage == data['patStage'])
        return condtion

    #过滤基因突变
    def filter_genes(self,genes):
        mole_detecs = MoleDetec.query.filter_by(pid=self.id).all()
        gene_record = []
        for mole_detec in mole_detecs:
            if mole_detec.ALK == 1:
                gene_record.append('ALK')
            if mole_detec.BIM == 1:
                gene_record.append('BIM')
            if mole_detec.BRAF == 1:
                gene_record.append('BRAF')
            if mole_detec.cMET == 1:
                gene_record.append('cMET')
            if mole_detec.EGFR == 1:
                gene_record.append('EGFR')
            if mole_detec.HER_2 == 1:
                gene_record.append('HER_2')
            if mole_detec.KRAS == 1:
                gene_record.append('KRAS')
            if mole_detec.PIK3CA == 1:
                gene_record.append('PIK3CA')
            if mole_detec.ROS1 == 1:
                gene_record.append('ROS1')
            if mole_detec.RET == 1:
                gene_record.append('RET')
            if mole_detec.UGT1A1 == 1:
                gene_record.append('UGT1A1')
        gene_record = list(set(gene_record)) #去重
        for gene in genes:
            if gene not in gene_record:
                return None
        return self

    def filter_age(self,age1,age2):
        if self.idNumber is None or self.idNumber == "":
            return None
        birth = get_birth_date_by_id_card(self.idNumber)
        age = get_age_by_birth(birth)
        if age is None or age < age1 or age > age2:
            return None
        return self

    def filter_PDL(self,PDL1,PDL2):
        mole_detecs = MoleDetec.query.filter_by(pid=self.id).all()
        for mole_detec in mole_detecs:
            if mole_detec.PDL1 and mole_detec.PDL1 >= PDL1 and mole_detec.PDL1 <= PDL2:
                return self
        return None

    def filter_TMB(self,TMB1,TMB2):
        mole_detecs = MoleDetec.query.filter_by(pid=self.id).all()
        for mole_detec in mole_detecs:
            if mole_detec.TMB and float(mole_detec.TMB) >= TMB1 and float(mole_detec.TMB) <= TMB2:
                return self
        return None

    def filter_theapy_method(self,method):
        trement = method.get('trement')
        treSolu = method.get('treSolu')
        if trement is None:
            return None
        tre_recs = TreRec.query.filter_by(pid=self.id,trement=trement).all()
        if treSolu is None:
            return None if tre_recs == [] else self

        items = OneToFive.query.filter_by(pid=self.id).all()
        for item in items:
            had_treSolu = item.treSolu.split(',')
            if treSolu in had_treSolu:
                return self
        return None

    def filter_patDia(self,items):
        ini_dia_pro = IniDiaPro.query.filter_by(pid=self.id).first()
        if ini_dia_pro is None or ini_dia_pro.patDia is None:
            return None
        cur_patDia = ini_dia_pro.patDia.split(',')
        for item in items:
            if item not in cur_patDia:
                return None
        return self


    def filter_traSite(self,items):
        ini_dia_pro = IniDiaPro.query.filter_by(pid=self.id).first()
        if ini_dia_pro is None or ini_dia_pro.traSite is None:
            return None
        cur_traSite = ini_dia_pro.traSite.split(',')
        for item in items:
            if item not in cur_traSite:
                return None
        return self


# 病人既往史表
class PastHis(Base):
    __tablename__ = 'pastHis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    basDisHis = Column(String(100), comment='基础疾病史,多个以逗号分隔')
    infDisHis = Column(String(100), comment='传染疾病史,多个以逗号分隔')
    tumor = Column(Boolean, comment='肿瘤史（无、有）')
    tumHis = Column(String(100), comment='肿瘤史,多个以逗号分隔')
    tumorFam = Column(Boolean, comment='肿瘤家族史（无、有）')
    tumFamHis = Column(String(100), comment='肿瘤家族史,多个以逗号分隔')
    smoke = Column(Boolean, comment='是否吸烟')
    smokingHis = Column(JSON, comment='吸烟史, {stopSmoke: 是否戒烟, smokeDayAvg: 日平均吸烟量/支, smokeYearAvg: 累计吸烟时间/年,stopSmokeHis: 戒烟时间}')
    drink = Column(Boolean, comment='是否饮酒（否、是）')
    drinkingHis = Column(JSON, comment='饮酒史, {stopDrink: 是否戒酒, drinkDayAvg: 日平均饮酒量, drinkYearAvg: 累计饮酒时间/年,stopDrinkHis: 戒酒时间}')
    hormone = Column(Boolean, comment='是否长期使用激素')
    hormoneUseHis = Column(JSON, comment='激素使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')
    drug = Column(Boolean, comment='是否长期使用药物')
    drugUseHis = Column(JSON, comment='药物使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')

    def keys(self):
        return ['id','pid','basDisHis','infDisHis','tumor','tumHis','tumorFam','tumFamHis','smoke','smokingHis',
                'drink','drinkingHis','hormone','hormoneUseHis','drug','drugUseHis']

#激素史与药物史
class DrugHistory(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    type = Column(SmallInteger,comment='type=1,激素史，type = 0，其他药物史')
    drug_name = Column(String(255))
    drug_dose = Column(String(255))
    use_time = Column(Integer)

    def keys(self):
        return ['id','drug_name','drug_dose','use_time']







# 病人初诊过程信息表
class IniDiaPro(Base):
    __tablename__ = 'iniDiaPro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    PSScore = Column(Integer, comment='首诊PS评分0-4')
    cliniManifest = Column(String(40), comment='临床表现,多个以逗号分隔')
    videography = Column(Boolean, comment='影像学 0-周围型；1-中央型')
    part = Column(String(100), comment='部位,多个以逗号分隔')
    bioMet = Column(String(40), comment='活检方式,多个以逗号分隔')
    pleInv = Column(Boolean, comment='是否胸膜侵犯')
    speSite = Column(String(30), comment='标本部位')
    firVisDate = Column(Date, comment='初诊日期')
    patReDate = Column(Date, comment='病理报告日期')
    patNum = Column(Integer, comment='病理号')
    patDia = Column(String(10000), comment='病理诊断,多个以逗号分隔')
    patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    mitIma = Column(Integer, comment='核分裂像')
    comCar = Column(String(100), comment='复合性癌')
    necArea = Column(Float, comment='坏死面积')
    massSize = Column(String(100), comment='肿块大小')
    Ki67 = Column(Float, comment='Ki67')
    traSite = Column(String(100), comment='转移部位')
    TSize = Column(Float, comment='TSize')
    stage = Column(String(30), comment='分期情况')
    cStage = Column(JSON, comment='c分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    cliStage = Column(String(30), comment='临床分期')
    pStage = Column(JSON, comment='p分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    patStage = Column(String(30), comment='病理分期')
    cRemark = Column(Text(10000))
    pRemark = Column(Text(10000))

    def keys(self):
        return ["id","PSScore","cliniManifest","videography","part","bioMet","pleInv","speSite","firVisDate",
                "patReDate","patNum","patDia","patDiaOthers","mitIma","comCar","necArea","massSize","Ki67",
                "traSite","TSize","stage","cStage","cliStage","pStage","patStage",'cRemark','pRemark']