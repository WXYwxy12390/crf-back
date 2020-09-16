from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base

# 治疗记录及疗效评估表
class TreRec(Base):
    __tablename__ = 'treRec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='1-n，表示对应第x条治疗记录')
    trement = Column(String(30), comment='几线治疗（手术、放疗、其他、1-5）(one,two,three,four,five,surgery,radiotherapy,other)')
    date = Column(Date, comment='结束日期')
    beEffEvaDate = Column(Date, comment='最佳疗效评估日期')
    beEffEva = Column(String(10), comment='最佳疗效评估')
    proDate = Column(Date, comment='进展日期')
    proDes = Column(String(60), comment='进展描述')  # text

    def keys(self):
        return ['id','trement','date','beEffEvaDate','beEffEva','proDate','proDes']



#1-5线及其他表
class OneToFive(Base):
    __tablename__ = 'oneToFive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    isTre = Column(Integer, comment='是否加入临床治疗')
    clinTri = Column(String(40), comment='临床实验名称')
    treSolu = Column(String(100), comment='治疗方案,多个以逗号分隔(Chemotherapy,TargetedTherapy,ImmunityTherapy,AntivascularTherapy,Other)')
    spePlan = Column(String(60), comment='具体方案')
    begDate = Column(Date, comment='开始日期')
    endDate = Column(Date, comment='结束日期')
    isRepBio  = Column(Boolean, comment='是否重复活检')
    bioMet = Column(String(40), comment='活检方式')
    matPart = Column(String(40), comment='取材部位')
    specNum = Column(Integer, comment='标本库流水号')
    patDiaRes = Column(Text(10000), comment='病理诊断结果')
    patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    #patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    note = Column(String(60), comment='备注')

#详细治疗方案
class DetailTrePlan(Base):
    __tablename__ = 'DetailTrePlan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    treSolu = Column(String(20), comment='治疗方案,Chemotherapy/TargetedTherapy/ImmunityTherapy/AntivascularTherapy/Other')
    treSche = Column(String(50),comment='药物方案')
    currPeriod = Column(Integer, comment='当前周期')
    treatName = Column(String(20), comment='治疗名称')
    begDate = Column(Date, comment='开始时间')
    endDate = Column(Date, comment='结束时间')
    drugs = Column(JSON, comment='药物使用情况, {drugName:{drugDosa: ,duration: },...}')
    note = Column(String(500), comment='药物使用备注')

    def keys(self):
        return ['id','treSolu','treSche','currPeriod','treatName','begDate','endDate','drugs','note']




#手术表
class Surgery(Base):
    __tablename__ = 'surgery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    surSco = Column(JSON, comment='手术范围')
    lymDis = Column(JSON, comment='淋巴清扫范围')
    cleGro = Column(String(40), comment='清扫组数')
    surDate = Column(Date, comment='手术日期')
    posAdjChem = Column(Boolean, comment='术后辅助化疗')
    isPro = Column(Boolean, comment='是否进展')
    proDate = Column(Date, comment='进展日期')
    proDes = Column(String(40), comment='进展描述')


#放疗表
class Radiotherapy(Base):
    __tablename__ = 'radiotherapy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    begDate = Column(Date, comment='开始日期')
    endDate = Column(Date, comment='结束日期')
    radSite = Column(JSON, comment='放疗部位')
    radDose = Column(Float, comment='放射剂量')
    dosUnit = Column(Boolean, comment='剂量单位,0: Gy, 1:cGy')
    splTim = Column(Integer, comment='分割次数')
    method = Column(String(5), comment='分割次数单位')





