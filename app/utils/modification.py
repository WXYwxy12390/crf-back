from app.libs.enums import ModuleStatus


def record_modification(item, data, pid, treNum, class_name):
    flag = if_status_allow_modification(pid, treNum, class_name, True)
    if not flag:
        return flag
    if item is None:
        return False
    modification_des = data['modification_des']
    # 删除该描述，剩下的都是修改的数据
    del data['modification_des']
    dic = {}
    # 在提交模块后，修改数据时会记录。但是此时都是一次只修改一个字段。
    for key, value in data.items():
        if key != 'id' and key != 'pid' and key != 'treNum':
            dic['column'] = key
            dic['content'] = value
            dic['description'] = modification_des
    item.record_modification(dic)
    return flag


# if_record表示是否要记录修改。
# 若是不记录修改的情况if_record是False，则该方法都会返回True。
# 若要记录修改if_record是True，则要根据模块状态判断是否可以。
def if_status_allow_modification(pid, treNum, class_name, if_record):
    flag = False  # 标志该模块的状态是否允许修改数据
    treNum_str = str(treNum)
    module = get_module_by_class_name(class_name)

    from app.models.base_line import Patient
    patient = Patient.query.get_or_404(pid)
    module_status = patient.module_status
    if if_record and module_status.get(module) is None:
        return flag
    if if_record and module_status[module].get(treNum_str) is None:
        return flag
    # 在记录修改的情况下，状态若是未提交或已结束，则不允许修改数据
    if if_record and module_status[module].get(treNum_str) in [ModuleStatus.UnSubmitted.value,
                                                               ModuleStatus.CRAFinish.value]:
        return flag

    if not if_record and module_status is not None and module_status.get(module) is not None \
            and module_status[module].get(treNum_str) is not None \
            and module_status[module][treNum_str] != ModuleStatus.UnSubmitted.value:
        return flag

    flag = True
    return flag


def get_module_by_class_name(class_name):
    module = class_name
    if class_name == 'TreRec':
        module = 'Evaluation'
    if module in ['OneToFive', 'Surgery', 'Radiotherapy', 'DetailTrePlan']:
        module = 'TreRec'
    if module == 'DrugHistory':
        module = 'PastHis'
    return module
