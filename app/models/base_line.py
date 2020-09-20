from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime, SmallInteger

from app.models.base import Base
# 病人基本信息表
class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='病人id')
    patNumber = Column(String(20), comment='编号')
    account = Column(String(40), comment='录入人,多个以逗号分隔,格式为(,17,23,)')
    researchCenter = Column(String(20), comment='研究中心,多个以逗号分隔,格式为(,17,23,)')
    idNumber = Column(String(18), comment='身份证号', unique=True)
    hospitalNumber = Column(String(20), comment='住院号')
    patientName = Column(String(100), comment='姓名')
    gender = Column(String(2), comment='性别')      #格式问题
    birthday = Column(Date, comment='出生日期')
    phoneNumber1 = Column(String(20), comment='电话号码1')
    phoneNumber2 = Column(String(20), comment='电话号码2')
    updateTime = Column(DateTime, comment='更新时间')
    nextFollowupTime = Column(DateTime, comment='随访时间')
    finishFollowup = Column(Integer, comment='是否完成随访(True:1、False:0)')

    def keys(self):
        return ['id','patNumber','account','researchCenter','idNumber','hospitalNumber',
                    'patientName','gender','birthday','phoneNumber1','phoneNumber2','updateTime','nextFollowupTime','finishFollowup']

    def get_fotmat_info(self):
        data = {
            'id':self.id,
            'patNumber':self.patNumber,
            'hospitalNumber':self.hospitalNumber,
            'patientName':self.patientName,
            'idNumber':self.idNumber,
            'phoneNumber':self.phoneNumber1,
            'gender':self.gender,
            'patDia':'xxx'
        }
        return data







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

    def keys(self):
        return ["id","PSScore","cliniManifest","videography","part","bioMet","pleInv","speSite","firVisDate",
                "patReDate","patNum","patDia","patDiaOthers","mitIma","comCar","necArea","massSize","Ki67",
                "traSite","TSize","stage","cStage","cliStage","pStage","patStage"]