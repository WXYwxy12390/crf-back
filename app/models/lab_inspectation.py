from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime

from app.models.base import Base


# 血常规表
class BloodRoutine(Base):
    __tablename__ = 'bloodRoutine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    RBC = Column(Float, comment='红细胞计数')
    HGb = Column(Float, comment='血红蛋白')
    HCT = Column(Float, comment='红细胞压积')
    MCV = Column(Float, comment='平均RBC体积')
    MCH = Column(Float, comment='RBC平均HGB')
    MCHC = Column(Float, comment='平均HGB浓度')
    RDWCV = Column(Float, comment='RBC分布宽度-CV')
    RDWSD = Column(Float, comment='RBC分布宽度-SD	')
    WBC = Column(Float, comment='白细胞计数	')
    GRAN_ = Column(Float, comment='中性粒细胞计数')
    LYM_ = Column(Float, comment='淋巴细胞计数')
    EOS_ = Column(Float, comment='嗜酸性粒细胞计数')
    MID_ = Column(Float, comment='单核细胞计数')
    BASO_ = Column(Float, comment='嗜碱性粒细胞计数')
    PLT = Column(Float, comment='血小板计数')
    LYM = Column(Float, comment='淋巴细胞%')
    MID = Column(Float, comment='单核细胞%')
    GRAN = Column(Float, comment='中性粒细胞%')
    EOS = Column(Float, comment='嗜酸性粒细胞%')
    BASO = Column(Float, comment='嗜碱性粒细胞%')
    NEUT = Column(Float, comment='中性淋巴比值')
    RBCMea = Column(Integer, comment='红细胞计数临床意义判定')
    HGbMea = Column(Integer, comment='血红蛋白临床意义判定')
    HCTMea = Column(Integer, comment='红细胞压积临床意义判定')
    MCVMea = Column(Integer, comment='平均RBC体积临床意义判定')
    MCHMea = Column(Integer, comment='RBC平均HGB临床意义判定')
    MCHCMea = Column(Integer, comment='平均HGB浓度临床意义判定')
    RDWCVMea = Column(Integer, comment='RBC分布宽度-CV临床意义判定')
    RDWSDMea = Column(Integer, comment='RBC分布宽度-SD临床意义判定')
    WBCMea = Column(Integer, comment='白细胞计数临床意义判定')
    GRAN_Mea = Column(Integer, comment='中性粒细胞计数临床意义判定	')
    LYM_Mea = Column(Integer, comment='淋巴细胞计数临床意义判定	')
    EOS_Mea = Column(Integer, comment='嗜酸性粒细胞计数临床意义判定')
    MID_Mea = Column(Integer, comment='单核细胞计数临床意义判定')
    BASO_Mea = Column(Integer, comment='嗜碱性粒细胞计数临床意义判定')
    PLTMea = Column(Integer, comment='血小板计数临床意义判定')
    LYMMea = Column(Integer, comment='淋巴细胞%临床意义判定')
    MIDMea = Column(Integer, comment='单核细胞%临床意义判定')
    GRANMea = Column(Integer, comment='中性粒细胞%临床意义判定')
    EOSMea = Column(Integer, comment='嗜酸性粒细胞%临床意义判定')
    BASOMea = Column(Integer, comment='嗜碱性粒细胞%临床意义判定')
    NEUTMea = Column(Integer, comment='中性淋巴比值临床意义判定')
    RBCNote = Column(Text(10000), comment='红细胞计数备注')
    HGbNote = Column(Text(10000), comment='血红蛋白备注')
    HCTNote = Column(Text(10000), comment='红细胞压积备注')
    MCVNote = Column(Text(10000), comment='平均RBC体积备注')
    MCHNote = Column(Text(10000), comment='RBC平均HGB备注')
    MCHCNote = Column(Text(10000), comment='平均HGB浓度备注')
    RDWCVNote = Column(Text(10000), comment='RBC分布宽度-CV备注')
    RDWSDNote = Column(Text(10000), comment='RBC分布宽度-SD备注')
    WBCNote = Column(Text(10000), comment='白细胞计数备注')
    GRAN_Note = Column(Text(10000), comment='中性粒细胞计数备注')
    LYM_Note = Column(Text(10000), comment='淋巴细胞计数备注')
    EOS_Note = Column(Text(10000), comment='嗜酸性粒细胞计数备注')
    MID_Note = Column(Text(10000), comment='单核细胞计数备注')
    BASO_Note = Column(Text(10000), comment='嗜碱性粒细胞计数备注')
    PLTNote = Column(Text(10000), comment='血小板计数备注')
    LYMNote = Column(Text(10000), comment='淋巴细胞%备注')
    MIDNote = Column(Text(10000), comment='单核细胞%备注')
    GRANNote = Column(Text(10000), comment='中性粒细胞%备注')
    EOSNote = Column(Text(10000), comment='嗜酸性粒细胞%备注')
    BASONote = Column(Text(10000), comment='嗜碱性粒细胞%备注')
    NEUTNote = Column(Text(10000), comment='中性淋巴比值备注')
    filePath = Column(Text(10000), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'RBC', 'HGb', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDWCV',
                'RDWSD', 'WBC', 'GRAN_', 'LYM_', 'EOS_', 'MID_', 'BASO_','PLT','LYM','MID','GRAN','EOS','BASO',
                'NEUT', 'RBCMea', 'HGbMea', 'HCTMea',
                'MCVMea', 'MCHMea', 'MCHCMea', 'WBCMea', 'GRAN_Mea', 'LYM_Mea', 'EOS_Mea', 'MID_Mea', 'BASO_Mea',
                'PLTMea', 'LYMMea', 'MIDMea', 'GRANMea', 'EOSMea', 'BASOMea', 'NEUTMea', 'RBCNote', 'HGbNote',
                'HCTNote','MCVNote', 'MCHNote', 'MCHCNote', 'RDWCVNote', 'RDWSDNote', 'WBCNote', 'GRAN_Note', 'LYM_Note',
                'EOS_Note','MID_Note', 'BASO_Note', 'PLTNote', 'LYMNote', 'MIDNote', 'GRANNote', 'EOSNote', 'BASONote',
                'NEUTNote','filePath']



# 血生化表
class BloodBio(Base):
    __tablename__ = 'bloodBio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    TP = Column(Float, comment='总蛋白')
    ALB = Column(Float, comment='白蛋白')
    GLO = Column(Float, comment='球蛋白')
    ALT = Column(Float, comment='丙氨酸氨基转移酶')
    AST = Column(Float, comment='门冬氨酸氨基转氨酶')
    LDH = Column(Float, comment='乳酸脱氢酶')
    GGT = Column(Float, comment='谷氨酰基转肽酶')
    TBIL = Column(Float, comment='谷氨酰基转肽酶')
    DBIL = Column(Float, comment='直接胆红素')
    IBIL = Column(Float, comment='间接胆红素')
    GLU = Column(Float, comment='血糖')
    TC = Column(Float, comment='总胆固醇')
    LDL = Column(Float, comment='低密度脂蛋白')
    hDL = Column(Float, comment='高密度脂蛋白')
    TG = Column(Float, comment='甘油三酯')
    UREA = Column(Float, comment='尿素')
    ALP = Column(Float, comment='碱性磷酸酶')
    CREA = Column(Float, comment='肌酐')
    UA = Column(Float, comment='尿酸')
    CO2 = Column(Float, comment='二氧化碳')
    K = Column(Float, comment='钾')
    Na = Column(Float, comment='钠')
    Cl = Column(Float, comment='氯')
    Ca = Column(Float, comment='钙')
    Mg = Column(Float, comment='镁')
    P = Column(Float, comment='磷')
    TPMea = Column(Integer, comment='总蛋白临床意义判定')
    ALBMea = Column(Integer, comment='白蛋白临床意义判定')
    GLOMea = Column(Integer, comment='球蛋白临床意义判定')
    ALTMea = Column(Integer, comment='丙氨酸氨基转移酶临床意义判定')
    ASTMea = Column(Integer, comment='门冬氨酸氨基转氨酶临床意义判定')
    LDHMea = Column(Integer, comment='乳酸脱氢酶临床意义判定')
    GGTMea = Column(Integer, comment='谷氨酰基转肽酶临床意义判定')
    TBILMea = Column(Integer, comment='总胆红素临床意义判定')
    DBILMea = Column(Integer, comment='直接胆红素临床意义判定')
    IBILMea = Column(Integer, comment='间接胆红素临床意义判定')
    GLUMea = Column(Integer, comment='血糖临床意义判定')
    TCMea = Column(Integer, comment='总胆固醇临床意义判定')
    LDLMea = Column(Integer, comment='低密度脂蛋白临床意义判定')
    hDLMea = Column(Integer, comment='高密度脂蛋白临床意义判定')
    TGMea = Column(Integer, comment='甘油三酯临床意义判定')
    UREAMea = Column(Integer, comment='尿素临床意义判定')
    ALPMea = Column(Integer, comment='碱性磷酸酶临床意义判定')
    CREAMea = Column(Integer, comment='肌酐临床意义判定')
    UAMea = Column(Integer, comment='尿酸临床意义判定')
    CO2Mea = Column(Integer, comment='二氧化碳临床意义判定')
    KMea = Column(Integer, comment='钾临床意义判定')
    NaMea = Column(Integer, comment='钠临床意义判定')
    ClMea = Column(Integer, comment='氯临床意义判定')
    CaMea = Column(Integer, comment='钙临床意义判定')
    MgMea = Column(Integer, comment='镁临床意义判定')
    PMea = Column(Integer, comment='磷临床意义判定')
    TPNote = Column(Text(10000), comment='总蛋白备注')
    ALBNote = Column(Text(10000), comment='白蛋白备注')
    GLONote = Column(Text(10000), comment='球蛋白备注')
    ALTNote = Column(Text(10000), comment='丙氨酸氨基转移酶备注')
    ASTNote = Column(Text(10000), comment='门冬氨酸氨基转氨酶备注')
    LDHNote = Column(Text(10000), comment='乳酸脱氢酶备注')
    GGTNote = Column(Text(10000), comment='谷氨酰基转肽酶备注')
    TBILNote = Column(Text(10000), comment='总胆红素备注')
    DBILNote = Column(Text(10000), comment='直接胆红素备注')
    IBILNote = Column(Text(10000), comment='间接胆红素备注')
    GLUNote = Column(Text(10000), comment='血糖备注')
    TCNote = Column(Text(10000), comment='总胆固醇备注')
    LDLNote = Column(Text(10000), comment='低密度脂蛋白备注')
    hDLNote = Column(Text(10000), comment='高密度脂蛋白备注')
    TGNote = Column(Text(10000), comment='甘油三酯备注')
    UREANote = Column(Text(10000), comment='尿素备注')
    ALPNote = Column(Text(10000), comment='碱性磷酸酶备注')
    CREANote = Column(Text(10000), comment='肌酐备注')
    UANote = Column(Text(10000), comment='尿酸备注')
    CO2Note = Column(Text(10000), comment='二氧化碳备注')
    KNote = Column(Text(10000), comment='钾备注')
    NaNote = Column(Text(10000), comment='钠备注')
    ClNote = Column(Text(10000), comment='氯备注')
    CaNote = Column(Text(10000), comment='钙备注')
    MgNote = Column(Text(10000), comment='镁备注')
    PNote = Column(Text(10000), comment='磷备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'TP', 'ALB', 'GLO', 'ALT', 'AST', 'LDH', 'GGT',
                'TBIL', 'DBIL', 'IBIL', 'GLU', 'TC', 'LDL', 'hDL', 'TG', 'UREA', 'ALP', 'CREA',
                'UA', 'CO2', 'K', 'Na', 'Cl', 'Ca', 'Mg', 'P', 'TPMea',
                'ALBMea', 'GLOMea', 'ALTMea', 'ASTMea', 'LDHMea', 'GGTMea', 'TBILMea', 'DBILMea', 'IBILMea',
                'GLUMea','TCMea', 'LDLMea', 'hDLMea', 'TGMea', 'UREAMea', 'ALPMea', 'CREAMea', 'UAMea',
                'CO2Mea','KMea', 'NaMea', 'ClMea', 'CaMea', 'MgMea', 'PMea', 'TPNote', 'ALBNote',
                'GLONote','ALTNote','ASTNote','LDHNote','GGTNote','TBILNote','DBILNote','IBILNote','GLUNote','TCNote',
                'LDLNote','hDLNote','TGNote','UREANote','ALPNote','CREANote','UANote','CO2Note','KNote','NaNote',
                'ClNote','CaNote', 'MgNote','PNote','filePath']


# 甲状腺功能表
class Thyroid(Base):
    __tablename__ = 'thyroid'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    FT3 = Column(Float, comment='游离三碘甲状腺原氨酸')
    FT4 = Column(Float, comment='游离甲状腺素')
    TSH = Column(Float, comment='促甲状腺激素')
    FT3Mea = Column(Integer, comment='游离三碘甲状腺原氨酸临床意义判定')
    FT4Mea = Column(Integer, comment='游离甲状腺素临床意义判定')
    TSHMea = Column(Integer, comment='促甲状腺激素临床意义判定')
    FT3Note = Column(Text(10000), comment='游离三碘甲状腺原氨酸备注')
    FT4Note = Column(Text(10000), comment='游离甲状腺素备注')
    TSHNote = Column(Text(10000), comment='促甲状腺激素备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'FT3', 'FT4', 'TSH', 'FT3Mea', 'FT4Mea', 'TSHMea', 'FT3Note',
                'FT4Note', 'TSHNote', 'filePath']

# 凝血功能表
class Coagulation(Base):
    __tablename__ = 'coagulation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    PT = Column(Float, comment='凝血酶原时间')
    APTT = Column(Float, comment='活化部分凝血酶时间')
    TT = Column(Float, comment='凝血酶时间')
    FIB = Column(Float, comment='纤维蛋白原浓度')
    INR = Column(Float, comment='国际标准化比值')
    D_dimer = Column(Float, comment='D-二聚体')
    PTMea = Column(Integer, comment='凝血酶原时间临床意义判定')
    APTTMea = Column(Integer, comment='活化部分凝血酶时间临床意义判定')
    TTMea = Column(Integer, comment='凝血酶时间临床意义判定')
    FIBMea = Column(Integer, comment='纤维蛋白原浓度临床意义判定')
    INRMea = Column(Integer, comment='国际标准化比值临床意义判定')
    D_dimer_Mea = Column(Integer, comment='D-二聚体临床意义判定')
    PTNote = Column(Text(10000), comment='凝血酶原时间备注')
    APTTNote = Column(Text(10000), comment='活化部分凝血酶时间备注')
    TTNote = Column(Text(10000), comment='凝血酶时间备注')
    FIBNote = Column(Text(10000), comment='纤维蛋白原浓度备注')
    INRNote = Column(Text(10000), comment='国际标准化比值备注')
    D_dimer_Note = Column(Text(10000), comment='D-二聚体备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'PT', 'APTT', 'TT', 'FIB', 'INR', 'D_dimer', 'PTMea',
                'APTTMea', 'TTMea', 'FIBMea','INRMea', 'D_dimer_Mea', 'PTNote', 'APTTNote', 'TTNote', 'FIBNote',
                'INRNote', 'D_dimer_Note', 'filePath']

# 心肌酶谱表
class MyocardialEnzyme(Base):
    __tablename__ = 'myocardialEnzyme'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    LDH = Column(Float, comment='乳酸脱氢酶')
    CK = Column(Float, comment='肌酸激酶')
    CK_MB = Column(Float, comment='肌酸激酶同工酶')
    cTnI = Column(Float, comment='心肌肌钙蛋白I')
    cTnT = Column(Float, comment='心肌肌钙蛋白T')
    MYO = Column(Float, comment='肌红蛋白')
    BNP = Column(Float, comment='脑钠肽')
    NT_proBNP = Column(Float, comment='氨基末端脑钠肽前体')
    LDHMea = Column(Integer, comment='乳酸脱氢酶临床意义判定')
    CKMea = Column(Integer, comment='肌酸激酶临床意义判定')
    CK_MBMea = Column(Integer, comment='肌酸激酶同工酶临床意义判定')
    cTnIMea = Column(Integer, comment='心肌肌钙蛋白I临床意义判定')
    cTnTMea = Column(Integer, comment='心肌肌钙蛋白T临床意义判定')
    MYOMea = Column(Integer, comment='肌红蛋白临床意义判定')
    BNPMea = Column(Integer, comment='脑钠肽临床意义判定')
    NT_proBNPMea = Column(Integer, comment='氨基末端脑钠肽前体临床意义判定')
    LDHNote = Column(Text(10000), comment='乳酸脱氢酶备注')
    CKNote = Column(Text(10000), comment='肌酸激酶备注')
    CK_MBNote = Column(Text(10000), comment='肌酸激酶同工酶备注')
    cTnINote = Column(Text(10000), comment='心肌肌钙蛋白I备注')
    cTnTNote = Column(Text(10000), comment='心肌肌钙蛋白T备注')
    MYONote = Column(Text(10000), comment='肌红蛋白备注')
    BNPNote = Column(Text(10000), comment='脑钠肽备注')
    NT_proBNPNote = Column(Text(10000), comment='氨基末端脑钠肽前体备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'LDH', 'CK', 'CK_MB', 'cTnI', 'cTnT', 'MYO', 'BNP',
                'NT_proBNP', 'LDHMea', 'CKMea','CK_MBMea', 'cTnIMea', 'cTnTMea', 'MYOMea', 'BNPMea', 'NT_proBNPMea',
                'LDHNote', 'CKNote', 'CK_MBNote','cTnINote', 'cTnTNote', 'MYONote', 'BNPNote', 'NT_proBNPNote', 'filePath']


# 细胞因子表
class Cytokines(Base):
    __tablename__ = 'Cytokines'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    TNF_a = Column(Float, comment='肿瘤坏死因子a')
    IL_1b = Column(Float, comment='白介素1b')
    IL_2R = Column(Float, comment='白介素2受体')
    IL_6 = Column(Float, comment='白介素6')
    IL_8 = Column(Float, comment='白介素8')
    IL_10 = Column(Float, comment='白介素10')
    TNF_aMea = Column(Integer, comment='肿瘤坏死因子a临床意义判定')
    IL_1bMea = Column(Integer, comment='白介素1b临床意义判定')
    IL_2RMea = Column(Integer, comment='白介素2受体临床意义判定')
    IL_6Mea = Column(Integer, comment='白介素6临床意义判定')
    IL_8Mea = Column(Integer, comment='白介素8临床意义判定')
    IL_10Mea = Column(Integer, comment='白介素10临床意义判定')
    TNF_aNote = Column(Text(10000), comment='肿瘤坏死因子a备注')
    IL_1bNote = Column(Text(10000), comment='白介素1b备注')
    IL_2RNote = Column(Text(10000), comment='白介素2受体备注')
    IL_6Note = Column(Text(10000), comment='白介素6备注')
    IL_8Note = Column(Text(10000), comment='白介素8备注')
    IL_10Note = Column(Text(10000), comment='白介素10备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'TNF_a', 'IL_1b', 'IL_2R', 'IL_6', 'IL_8', 'IL_10', 'TNF_aMea',
                'IL_1bMea', 'IL_2RMea', 'IL_6Mea','IL_8Mea', 'IL_10Mea', 'TNF_aNote', 'IL_1bNote', 'IL_2RNote', 'IL_6Note',
                'IL_8Note', 'IL_10Note', 'filePath']


# 淋巴细胞亚群表
class LymSubsets(Base):
    __tablename__ = 'lymSubsets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    CD19_ = Column(Float, comment='B淋巴细胞绝对值')
    CD3_ = Column(Float, comment='T淋巴细胞绝对值')
    CD4_ = Column(Float, comment='Th淋巴细胞绝对值')
    CD8_ = Column(Float, comment='Ts淋巴细胞绝对值')
    CD16_56 = Column(Float, comment='自然杀伤细胞绝对值')
    LYMPH_ = Column(Float, comment='淋巴细胞数')
    CD19 = Column(Float, comment='B淋巴细胞')
    CD3 = Column(Float, comment='T淋巴细胞')
    CD4 = Column(Float, comment='Th淋巴细胞')
    CD8 = Column(Float, comment='Ts淋巴细胞')
    CD4CD8 = Column(Float, comment='Th淋巴细胞/ Ts淋巴细胞')
    CD56 = Column(Float, comment='自然杀伤细胞')
    CD3_CD8__ = Column(Float, comment='CD3+CD8+绝对值')
    CD3_CD8_ = Column(Float, comment='CD3+CD8+')
    CD3_CD4__ = Column(Float, comment='CD3+CD4+绝对值')
    CD3_CD4_ = Column(Float, comment='CD3+CD4+')
    CD3_CD16_56_ = Column(Float, comment='CD3-CD(16+56)绝对值')
    CD3_CD16_56 = Column(Float, comment='CD3-CD(16+56) ')
    CD3_CD19__ = Column(Float, comment='CD3-CD19+绝对值')
    CD3_CD19_ = Column(Float, comment='CD3-CD19+')
    CD8_CD28_ = Column(Float, comment='CD8+CD28+')
    CD20_ = Column(Float, comment='CD20+')
    HLA_DR_ = Column(Float, comment='HLA-DR+')
    CD3_HLA_DR1 = Column(Float, comment='CD3+/HLA-DR+')
    CD3_HLA_DR2 = Column(Float, comment='CD3+/HLA-DR-')
    CD3_HLA_DR3 = Column(Float, comment='CD3-/HLA-DR+')
    CD4_CD25_CD127low = Column(Float, comment='CD4+CD25+CD127low')
    CD19_Mea = Column(Integer, comment='B淋巴细胞绝对值临床意义判定')
    CD3_Mea = Column(Integer, comment='T淋巴细胞绝对值临床意义判定')
    CD4_Mea = Column(Integer, comment='Th淋巴细胞绝对值临床意义判定')
    CD8_Mea = Column(Integer, comment='Ts淋巴细胞绝对值临床意义判定')
    CD16_56Mea = Column(Integer, comment='自然杀伤细胞绝对值临床意义判定')
    LYMPH_Mea = Column(Integer, comment='淋巴细胞数临床意义判定')
    CD19Mea = Column(Integer, comment='B淋巴细胞临床意义判定')
    CD3Mea = Column(Integer, comment='T淋巴细胞临床意义判定')
    CD4Mea = Column(Integer, comment='Th淋巴细胞临床意义判定')
    CD8Mea = Column(Integer, comment='Ts淋巴细胞临床意义判定')
    CD4CD8Mea = Column(Integer, comment='Th淋巴细胞/ Ts淋巴细胞临床意义判定')
    CD56Mea = Column(Integer, comment='自然杀伤细胞临床意义判定')
    CD3_CD8__Mea = Column(Integer, comment='CD3+CD8+绝对值临床意义判定')
    CD3_CD8_Mea = Column(Integer, comment='CD3+CD8+临床意义判定')
    CD3_CD4__Mea = Column(Integer, comment='CD3+CD4+绝对值临床意义判定')
    CD3_CD4_Mea = Column(Integer, comment='CD3+CD4+临床意义判定')
    CD3_CD16_56_Mea = Column(Integer, comment='CD3-CD(16+56)绝对值临床意义判定')
    CD3_CD16_56Mea = Column(Integer, comment='CD3-CD(16+56) 临床意义判定')
    CD3_CD19__Mea = Column(Integer, comment='CD3-CD19+绝对值临床意义判定')
    CD3_CD19_Mea = Column(Integer, comment='CD3-CD19+临床意义判定')
    CD8_CD28_Mea = Column(Integer, comment='CD8+CD28+临床意义判定')
    CD20_Mea = Column(Integer, comment='CD20+临床意义判定')
    HLA_DR_Mea = Column(Integer, comment='HLA-DR+临床意义判定')
    CD3_HLA_DR1Mea = Column(Integer, comment='CD3+/HLA-DR+临床意义判定')
    CD3_HLA_DR2Mea = Column(Integer, comment='CD3+/HLA-DR-临床意义判定')
    CD3_HLA_DR3Mea = Column(Integer, comment='CD3-/HLA-DR+临床意义判定')
    CD4_CD25_CD127lowMea = Column(Integer, comment='CD4+CD25+CD127low临床意义判定')
    CD19_Note = Column(Text(10000), comment='B淋巴细胞绝对值备注')
    CD3_Note = Column(Text(10000), comment='T淋巴细胞绝对值备注')
    CD4_Note = Column(Text(10000), comment='Th淋巴细胞绝对值备注')
    CD8_Note = Column(Text(10000), comment='Ts淋巴细胞绝对值备注')
    CD16_56Note = Column(Text(10000), comment='自然杀伤细胞绝对值备注')
    LYMPH_Note = Column(Text(10000), comment='淋巴细胞数备注')
    CD19Note = Column(Text(10000), comment='B淋巴细胞备注')
    CD3Note = Column(Text(10000), comment='T淋巴细胞备注')
    CD4Note = Column(Text(10000), comment='Th淋巴细胞备注')
    CD8Note = Column(Text(10000), comment='Ts淋巴细胞备注')
    CD4CD8Note = Column(Text(10000), comment='Th淋巴细胞/ Ts淋巴细胞备注')
    CD56Note = Column(Text(10000), comment='自然杀伤细胞备注')
    CD3_CD8__Note = Column(Text(10000), comment='CD3+CD8+绝对值备注')
    CD3_CD8_Note = Column(Text(10000), comment='CD3+CD8+备注')
    CD3_CD4__Note = Column(Text(10000), comment='CD3+CD4+绝对值备注')
    CD3_CD4_Note = Column(Text(10000), comment='CD3+CD4+备注')
    CD3_CD16_56_Note = Column(Text(10000), comment='CD3-CD(16+56)绝对值备注')
    CD3_CD16_56Note = Column(Text(10000), comment='CD3-CD(16+56) 备注')
    CD3_CD19__Note = Column(Text(10000), comment='CD3-CD19+绝对值备注')
    CD3_CD19_Note = Column(Text(10000), comment='CD3-CD19+备注')
    CD8_CD28_Note = Column(Text(10000), comment='CD8+CD28+备注')
    CD20_Note = Column(Text(10000), comment='CD20+备注')
    HLA_DR_Note = Column(Text(10000), comment='HLA-DR+备注')
    CD3_HLA_DR1Note = Column(Text(10000), comment='CD3+/HLA-DR+备注')
    CD3_HLA_DR2Note = Column(Text(10000), comment='CD3+/HLA-DR-备注')
    CD3_HLA_DR3Note = Column(Text(10000), comment='CD3-/HLA-DR+备注')
    CD4_CD25_CD127lowNote = Column(Text(10000), comment='CD4+CD25+CD127low备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'CD19_', 'CD3_', 'CD4_', 'CD8_', 'CD16_56', 'LYMPH_', 'CD19',
                'CD3', 'CD4', 'CD8', 'CD4CD8', 'CD56', 'CD3_CD8__', 'CD3_CD8_', 'CD3_CD4__', 'CD3_CD4_', 'CD3_CD16_56_', 'CD3_CD16_56',
                'CD3_CD19__', 'CD3_CD19_', 'CD8_CD28_', 'CD20_', 'HLA_DR_', 'CD3_HLA_DR1', 'CD3_HLA_DR2', 'CD3_HLA_DR3', 'CD4_CD25_CD127low',
                'CD19_Mea', 'CD3_Mea', 'CD4_Mea', 'CD8_Mea', 'CD16_56Mea', 'LYMPH_Mea', 'CD19Mea', 'CD3Mea', 'CD4Mea',
                'CD8Mea','CD4CD8Mea', 'CD56Mea', 'CD3_CD8__Mea', 'CD3_CD8_Mea', 'CD3_CD4__Mea', 'CD3_CD4_Mea', 'CD3_CD16_56_Mea', 'CD3_CD16_56Mea',
                'CD3_CD19__Mea','CD3_CD19_Mea', 'CD8_CD28_Mea', 'CD20_Mea', 'HLA_DR_Mea', 'CD3_HLA_DR1Mea', 'CD3_HLA_DR2Mea', 'CD3_HLA_DR3Mea', 'CD4_CD25_CD127lowMea',
                'CD19_Note','CD3_Note','CD4_Note','CD8_Note','CD16_56Note','LYMPH_Note','CD19Note','CD3Note','CD4Note','CD8Note',
                'CD4CD8Note','CD56Note','CD3_CD8__Note','CD3_CD8_Note','CD3_CD4__Note','CD3_CD4_Note','CD3_CD16_56_Note','CD3_CD16_56Note','CD3_CD19__Note','CD3_CD19_Note',
                'CD8_CD28_Note','CD20_Note', 'HLA_DR_Note','CD3_HLA_DR1Note','CD3_HLA_DR2Note','CD3_HLA_DR3Note','CD4_CD25_CD127lowNote','filePath']


# 尿常规表
class UrineRoutine(Base):
    __tablename__ = 'urineRoutine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    UPH = Column(String(20), comment='酸碱度')
    UGLU = Column(String(20), comment='尿糖')
    LEU = Column(String(20), comment='尿白细胞')
    ERY = Column(String(20), comment='尿红细胞')
    NIT = Column(String(20), comment='尿亚硝酸')
    BIL = Column(String(20), comment='尿胆红素')
    USG = Column(String(20), comment='尿比重')
    KET = Column(String(20), comment='尿酮体')
    BLD = Column(String(20), comment='尿隐血')
    PRO = Column(String(20), comment='尿蛋白')
    UBG = Column(String(20), comment='尿胆元')
    COL = Column(String(20), comment='尿颜色')
    CLA = Column(String(20), comment='尿透明度')
    UPHMea = Column(Integer, comment='酸碱度临床意义判定')
    UGLUMea = Column(Integer, comment='尿糖临床意义判定')
    LEUMea = Column(Integer, comment='尿白细胞临床意义判定')
    ERYMea = Column(Integer, comment='尿红细胞临床意义判定')
    NITMea = Column(Integer, comment='尿亚硝酸临床意义判定')
    BILMea = Column(Integer, comment='尿胆红素临床意义判定')
    USGMea = Column(Integer, comment='尿比重临床意义判定')
    KETMea = Column(Integer, comment='尿酮体临床意义判定')
    BLDMea = Column(Integer, comment='尿隐血临床意义判定')
    PROMea = Column(Integer, comment='尿蛋白临床意义判定')
    UBGMea = Column(Integer, comment='尿胆元临床意义判定')
    COLMea = Column(Integer, comment='尿颜色临床意义判定')
    CLAMea = Column(Integer, comment='尿透明度临床意义判定')
    UPHNote = Column(Text(10000), comment='酸碱度备注')
    UGLUNote = Column(Text(10000), comment='尿糖备注')
    LEUNote = Column(Text(10000), comment='尿白细胞备注')
    ERYNote = Column(Text(10000), comment='尿红细胞备注')
    NITNote = Column(Text(10000), comment='尿亚硝酸备注')
    BILNote = Column(Text(10000), comment='尿胆红素备注')
    USGNote = Column(Text(10000), comment='尿比重备注')
    KETNote = Column(Text(10000), comment='尿酮体备注')
    BLDNote = Column(Text(10000), comment='尿隐血备注')
    PRONote = Column(Text(10000), comment='尿蛋白备注')
    UBGNote = Column(Text(10000), comment='尿胆元备注')
    COLNote = Column(Text(10000), comment='尿颜色备注')
    CLANote = Column(Text(10000), comment='尿透明度备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'UPH', 'UGLU', 'LEU', 'ERY', 'NIT', 'BIL', 'USG',
                'KET', 'BLD', 'PRO', 'UBG', 'COL', 'CLA','UPHMea', 'UGLUMea', 'LEUMea', 'ERYMea', 'NITMea', 'BILMea', 'USGMea',
                'KETMea', 'BLDMea', 'PROMea', 'UBGMea', 'COLMea', 'CLAMea','UPHNote', 'UGLUNote', 'LEUNote', 'ERYNote', 'NITNote',
                'BILNote', 'USGNote','KETNote', 'BLDNote', 'PRONote', 'UBGNote', 'COLNote', 'CLANote','filePath']


# 肿瘤标志物表
class TumorMarker(Base):
    __tablename__ = 'tumorMarker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    samplingTime = Column(Date, comment='采样时间')
    CEA = Column(Float, comment='癌胚抗原')
    NSE = Column(Float, comment='神经元特异烯醇化酶')
    pro_GPR = Column(Float, comment='胃泌素释放肽前体')
    CYFRA = Column(Float, comment='CYFRA21-1')
    FERR = Column(Float, comment='铁蛋白')
    AFP = Column(Float, comment='甲胎蛋白')
    SCCA = Column(Float, comment='鳞癌相关抗原')
    CEAMea = Column(Integer, comment='癌胚抗原临床意义判定')
    NSEMea = Column(Integer, comment='神经元特异烯醇化酶临床意义判定')
    pro_GPRMea = Column(Integer, comment='胃泌素释放肽前体临床意义判定')
    CYFRAMea = Column(Integer, comment='CYFRA21-1临床意义判定')
    FERRMea = Column(Integer, comment='铁蛋白临床意义判定')
    AFPMea = Column(Integer, comment='甲胎蛋白临床意义判定')
    SCCAMea = Column(Integer, comment='鳞癌相关抗原临床意义判定')
    CEANote = Column(Text(10000), comment='癌胚抗原备注')
    NSENote = Column(Text(10000), comment='神经元特异烯醇化酶备注')
    pro_GPRNote = Column(Text(10000), comment='胃泌素释放肽前体备注')
    CYFRANote = Column(Text(10000), comment='CYFRA21-1备注')
    FERRNote = Column(Text(10000), comment='铁蛋白备注')
    AFPNote = Column(Text(10000), comment='甲胎蛋白备注')
    SCCANote = Column(Text(10000), comment='鳞癌相关抗原备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'samplingTime', 'CEA', 'NSE', 'pro_GPR', 'CYFRA', 'FERR', 'AFP', 'SCCA',
                'CEAMea', 'NSEMea', 'pro_GPRMea', 'CYFRAMea', 'FERRMea', 'AFPMea','SCCAMea', 'CEANote', 'NSENote', 'pro_GPRNote', 'CYFRANote', 'FERRNote',
                'AFPNote', 'SCCANote', 'filePath']
