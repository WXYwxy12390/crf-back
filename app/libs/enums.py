from enum import Enum


class ModuleStatus(Enum):
    # 模块的提交状态
    UnSubmitted = 0
    Submitted = 1
    Finished = 2
    WithQuery = 3
    AllReplied = 4

