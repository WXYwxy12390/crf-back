from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base, db


# 治疗记录及疗效评估表
from app.models.cycle import Immunohis, MoleDetec, Signs, SideEffect
from app.models.lab_inspectation import BloodRoutine, BloodBio, Thyroid, Coagulation, MyocardialEnzyme, Cytokines, \
    LymSubsets, UrineRoutine, TumorMarker
from app.models.other_inspect import Lung, OtherExams, ImageExams


class TreRec(Base):
    __tablename__ = 'treRec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='1-n，表示对应第x条治疗记录')
    trement = Column(String(255), comment='几线治疗（手术、放疗、其他、1-5）(one,two,three,four,five,surgery,radiotherapy,other)')
    date = Column(DateTime, comment='结束日期')
    beEffEvaDate = Column(Date, comment='最佳疗效评估日期')
    beEffEva = Column(String(255), comment='最佳疗效评估')
    proDate = Column(DateTime, comment='进展日期')
    proDes = Column(String(2048), comment='进展描述')  # text

    def keys(self):
        return ['id','treNum','trement','date','beEffEvaDate','beEffEva','proDate','proDes']

    def get_parent(self):
        data = {
            'id':self.id,
            'trement':self.trement
        }
        return data
    def get_child(self):
        trement = self.trement
        if trement in ['one','two','three','four','five','other']:
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

            #删除实验室检查
            self.delete_in_cycle(BloodRoutine)
            self.delete_in_cycle(BloodBio)
            self.delete_in_cycle(Thyroid)
            self.delete_in_cycle(Coagulation)
            self.delete_in_cycle(MyocardialEnzyme)
            self.delete_in_cycle(Cytokines)
            self.delete_in_cycle(LymSubsets)
            self.delete_in_cycle(UrineRoutine)
            self.delete_in_cycle(TumorMarker)

            #删除其他检查
            self.delete_in_cycle(Lung)
            self.delete_in_cycle(OtherExams)
            self.delete_in_cycle(ImageExams)

            #删除免疫组化，分子检测，症状体征，副反应
            self.delete_in_cycle(Immunohis)
            self.delete_in_cycle(MoleDetec)
            self.delete_in_cycle(Signs)
            self.delete_in_cycle(SideEffect)








    def delete_in_cycle(self,table):

        records = table.query.filter_by(pid=self.pid,treNum=self.treNum).all()
        with db.auto_commit():
            for record in records:
                record.delete()


#1-5线及其他表
class OneToFive(Base):
    __tablename__ = 'oneToFive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    isTre = Column(Integer, comment='是否加入临床治疗')
    clinTri = Column(String(40), comment='临床实验名称')  #长度
    treSolu = Column(String(100), comment='治疗方案,多个以逗号分隔(Chemotherapy,TargetedTherapy,ImmunityTherapy,AntivascularTherapy,Other)') #长度
    spePlan = Column(String(60), comment='具体方案')
    begDate = Column(Date, comment='开始日期')
    endDate = Column(Date, comment='结束日期')
    isRepBio  = Column(Boolean, comment='是否重复活检')
    bioMet = Column(JSON, comment='活检方式')   #长度
    _bioMet = Column(String(40), comment='活检方式')  # 长度
    matPart = Column(String(255), comment='取材部位') #长度
    specNum = Column(Integer, comment='标本库流水号')  #类型 改为字符串
    patDia = Column(JSON, comment='病理诊断结果')
    patDiaRes = Column(Text(10000), comment='病理诊断结果')
    patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    #patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')
    note = Column(String(2048), comment='备注')

    def keys(self):
        return ['id','pid','treNum','isTre','clinTri','treSolu','spePlan','begDate',
                'endDate','isRepBio','bioMet','matPart','specNum','patDiaRes','patDiaOthers','note','patDia',
                '_bioMet']


#详细治疗方案
class DetailTrePlan(Base):
    __tablename__ = 'DetailTrePlan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    treSolu = Column(String(255), comment='治疗方案,Chemotherapy/TargetedTherapy/ImmunityTherapy/AntivascularTherapy/Other')
    treSche = Column(String(255),comment='药物方案')    #长度
    currPeriod = Column(Integer, comment='当前周期')
    treatName = Column(String(255), comment='治疗名称') #长度
    begDate = Column(Date, comment='开始时间')
    endDate = Column(Date, comment='结束时间')
    drugs = Column(JSON, comment='药物使用情况, {drugName:{drugDosa: ,duration: },...}')
    note = Column(String(2048), comment='药物使用备注')  #长度

    def keys(self):
        return ['id','treSolu','treSche','currPeriod','treatName','begDate','endDate','drugs','note']




#手术表
class Surgery(Base):
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
    isRepBio  = Column(Boolean, comment='是否重复活检')
    # bioMet = Column(JSON, comment='活检方式')  # 长度
    bioMet = Column(JSON, comment='活检方式')  # 长度
    matPart = Column(String(255), comment='取材部位')
    specNum = Column(Integer, comment='标本库流水号')

    patDia = Column(JSON, comment='病理诊断结果')
    def keys(self):
        return ['id','pid','treNum','surSco','lymDis','cleGro','surDate','posAdjChem','isPro','proDate','proDes',
                'isRepBio','bioMet','matPart','specNum','patDia',
                '_surSco','_lymDis']
#放疗表
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
    specNum = Column(Integer, comment='标本库流水号')
    patDia = Column(JSON, comment='病理诊断结果')

    def keys(self):
        return ['id','pid','treNum','begDate','endDate','radSite','radDose','dosUnit','splTim','method','_radSite',
                'isRepBio','bioMet','matPart','specNum','patDia']





