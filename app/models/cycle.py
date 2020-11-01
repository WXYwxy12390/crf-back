from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base




# 病人免疫组化信息表
class Immunohis(Base):
    __tablename__ = 'immunohis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    ALKD5F3 = Column(Integer, comment='ALKD5F3 0:-,1:±,2:+,3:++,4:+++')
    ALKD5F3N = Column(Integer, comment='ALKD5F3-N')
    CAIX = Column(Integer, comment='CAIX')
    CAM52 = Column(Integer, comment='CAM5.2')
    CD10 = Column(Integer, comment='CD10')
    CD34 = Column(Integer, comment='CD34')
    CD56 = Column(Integer, comment='CD56')
    CD117 = Column(Integer, comment='CD117')
    CDX2 = Column(Integer, comment='CDX-2')
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
    other = Column(String(2048), comment='其他')      #长度
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'ALKD5F3', 'ALKD5F3N', 'CAIX', 'CAM52', 'CD10', 'CD34', 'CD56',
                'CD117', 'CDX2', 'CEA', 'CgA', 'CK', 'CK56','CK7', 'CK818', 'CK19', 'CK20', 'Cyn', 'DLL3', 'EMA',
                'ERCC1', 'LCA', 'MCM2', 'NapsinA', 'P16', 'P40','p53', 'P63', 'PAX2', 'PAX8', 'PCK',
                'PDL1', 'RRM1','SATB2', 'Syn', 'TTF1', 'VEGFC', 'Villin', 'Villinco','other','filePath']


# 病人分子检测信息表
class MoleDetec(Base):
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
    ALKSam = Column(String(255), comment='ALK检测样本')  #下面的文本都要改
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
    UGT1A1Desc = Column(String(255), comment='UGT1A1结果描述')  #长度
    path = Column(String(200), comment='报告文件路径')
    MSI = Column(Integer, comment='MSI 0-MSS,1-MSIH,2-MSIL')
    other = Column(Text)
    PDL1 = Column(Float, comment='PD-L1表达 0-未测,1-不详,2->50%,3-1%-50%,4-<1%,5-阴性')
    PDL1KT = Column(String(255), comment='PDL1抗体') #长度
    TMB = Column(String(20), comment='TMB') #???

    def keys(self):
        return ['id', 'pid', 'treNum', 'ALK', 'BIM', 'BRAF', 'cMET', 'EGFR', 'HER_2', 'KRAS',
                'PIK3CA', 'ROS1', 'RET', 'UGT1A1', 'ALKSam', 'BIMSam','BRAFSam','cMETSam', 'EGFRSam', 'HER_2Sam', 'KRASSam', 'PIK3CASam', 'ROS1Sam',
                'RETSam', 'UGT1A1Sam', 'ALKDetMed', 'BIMDetMed', 'BRAFDetMed', 'cMETDetMed','EGFRDetMed', 'HER_2DetMed', 'KRASDetMed', 'PIK3CADetMed', 'ROS1DetMed',
                'RETDetMed', 'UGT1A1DetMed','ALKDesc', 'BIMDesc', 'BRAFDesc', 'cMETDesc', 'EGFRDesc', 'HER_2Desc','KRASDesc','PIK3CADesc',
                'ROS1Desc','RETDesc','UGT1A1Desc','path','MSI','other','PDL1','PDL1KT','TMB']








#症状体征表
class Signs(Base):
    __tablename__ = 'signs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    symName = Column(String(255), comment='症状名称')
    begDate = Column(DateTime, comment='开始日期')
    isExe = Column(Integer, comment='目前是否存在')
    endDate = Column(DateTime, comment='结束日期')

    def keys(self):
        return ['id', 'pid', 'treNum', 'symName', 'begDate', 'isExe', 'endDate']

#副反应表
class SideEffect(Base):
    __tablename__ = 'sideEffect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='number,对应病人的某一条治疗记录')
    sidReaName = Column(String(255), comment='副反应名称')
    sidReaNameOther = Column(String(2048),comment='副反应其他名称') #随访数据库好像没有这字段了
    sidRecCla = Column(Integer, comment='副反应分级')
    begDate = Column(Date, comment='开始日期')
    isExe = Column(Integer, comment='目前是否存在')
    treatment = Column(String(2048), comment='治疗情况')
    endDate = Column(Date, comment='结束日期')

    def keys(self):
        return ['id', 'pid', 'treNum', 'sidReaName', 'sidRecCla', 'begDate', 'isExe','treatment','endDate','sidReaNameOther']