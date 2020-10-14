from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime
from app.models.base import Base


#随访信息表
class FollInfo(Base):
    __tablename__ = 'follInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    number = Column(Integer, comment='第n条记录')
    date = Column(DateTime, comment='时间')  #date
    effEva = Column(Integer, comment='疗效评估,1 : PD-进展, 2 : SD-稳定, 3 : PR-部分缓解, 4 : CR-完全缓解, 5 : 术后未发现新病灶')
    folMet = Column(Integer, comment='随访方式,1 : 电话, 2 : 门诊, 3 : 住院')
    livSta = Column(Integer, comment='生存状态, 1 : 死亡, 2 : 存活, 3 : 失联')
    remarks = Column(String(1000), comment='备注')
    imaFilType = Column(Integer, comment='影像文件类型, 1 : X光, 2 : 超声, 3 : CT, 4 : MRI, 5 : PET/CT')
    suv = Column(Float, comment='选择PET影像时记录其标准摄取值(standard uptake value ,SUV)')
    savFilPath = Column(String(200), comment='保存文件路径,多个以逗号分隔')
    examArea = Column(String(20), comment='检查部位') #废弃
    tumorLD = Column(Float, comment='肿瘤长径') #废弃
    tumorSD = Column(Float, comment='肿瘤短径') #废弃
    tumorDesc = Column(String(100), comment='肿瘤描述') #废弃

    def keys(self):
        return ['id', 'pid', 'number', 'date', 'effEva', 'folMet', 'livSta', 'remarks', 'imaFilType', 'suv', 'savFilPath',
                'examArea', 'examArea', 'tumorLD', 'tumorSD', 'tumorDesc']