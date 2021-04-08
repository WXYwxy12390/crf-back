from flask import request
from app.libs.redprint import Redprint
from app.utils.export3 import Export as Export3

api = Redprint('export')

models_package = __import__('app.models', fromlist=['XXX'])
base_line_py = getattr(models_package, 'base_line')
crf_info_py = getattr(models_package, 'crf_info')
cycle_py = getattr(models_package, 'cycle')
lab_inspectation_py = getattr(models_package, 'lab_inspectation')
other_inspect_py = getattr(models_package, 'other_inspect')
therapy_record_py = getattr(models_package, 'therapy_record')


@api.route('', methods=['POST'])
def export():
    data = request.get_json()
    keys = data.keys()
    pids = data['pids'] if 'pids' in keys else []
    treNums = data['treNums'] if 'treNums' in keys else []
    follInfoNum = data['follInfoNum'] if 'follInfoNum' in keys else 0
    baseLine = []
    trementInfo = []
    follInfo = {}
    if_baseLine_ok = True
    if_trementInfo_ok = True
    if_follInfo_ok = True
    if 'baseLine' in keys:
        baseLine = data['baseLine']
        if_baseLine_ok = check_tables_and_columns(baseLine)
    if 'trementInfo' in keys:
        trementInfo = data['trementInfo']
        if_trementInfo_ok = check_tables_and_columns(trementInfo)
    if 'follInfo' in keys:
        follInfo = data['follInfo']
        if if_table_exist(follInfo['table']) and if_columns_exist(if_table_exist(follInfo['table']),
                                                                  follInfo['column']):
            if_follInfo_ok = True
        else:
            if_follInfo_ok = False

    if if_baseLine_ok and if_trementInfo_ok and if_follInfo_ok:
        return Export3(pids, treNums, follInfoNum, baseLine, trementInfo, follInfo).work()
    else:
        print('接收的表名或者字段名存在错误')


# 检查json中的表名和字段名是否正确.
# 若正确返回tables,columns两个数组，若不正确返回None
def check_tables_and_columns(data):
    flag = True

    for k in range(0, len(data)):
        table = data[k].get('table')
        column = data[k].get('column')
        obj_class_name = if_table_exist(table)
        if obj_class_name:
            data[k]['table'] = obj_class_name
            if not if_columns_exist(obj_class_name, column):
                print('字段名不存在！')
                flag = False
                break
        else:
            print('表名不存在！')
            flag = False
            break
    if flag:
        return data
    else:
        return []


# 判断该名称的表在数据库中是否存在。
# 若存在，返回该表对应的模型类；若不存在，返回None
def if_table_exist(tableName):
    if hasattr(base_line_py, tableName):
        obj_class_name = getattr(base_line_py, tableName)
        return obj_class_name
    elif hasattr(crf_info_py, tableName):
        obj_class_name = getattr(crf_info_py, tableName)
        return obj_class_name
    elif hasattr(cycle_py, tableName):
        obj_class_name = getattr(cycle_py, tableName)
        return obj_class_name
    elif hasattr(lab_inspectation_py, tableName):
        obj_class_name = getattr(lab_inspectation_py, tableName)
        return obj_class_name
    elif hasattr(other_inspect_py, tableName):
        obj_class_name = getattr(other_inspect_py, tableName)
        return obj_class_name
    elif hasattr(therapy_record_py, tableName):
        obj_class_name = getattr(therapy_record_py, tableName)
        return obj_class_name
    else:
        return None


# 判断数组中的字段名是否都正确，
# obj为表对应的模型类；columns是字符串数组，存放若干个字段名
def if_columns_exist(obj_class_name, columns):
    flag = True
    for column in columns:
        export_header_map = getattr(obj_class_name, 'export_header_map')
        if not (column in export_header_map.keys()):
            flag = False
            break

    return flag
