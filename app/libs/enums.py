from enum import Enum


class ModuleStatus(Enum):
    # 模块的提交状态
    UnSubmitted = 0
    # 未启动监察
    UnInitiateMonitoring = 1
    # CRA监察中
    CRAMonitoring = 2
    # CRA有质疑
    CRADoubt = 3
    # 有回复
    WithReply = 4
    # CRA已完成
    CRAFinish = 5


class GeneValue(Enum):
    # 阳
    Yang = 1
    # 阴
    Yin = 0
    # 未知
    Unknown = 2
