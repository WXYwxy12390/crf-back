from flask import request
from app.libs.redprint import Redprint
from app.utils.export2 import Export as Export2
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
    pids = data['pids']
    maxTreNum = data['maxTreNum']
    minTreNum = data['minTreNum']

    treNums = []
    for i in range(minTreNum, maxTreNum + 1):
        treNums.append(i)

    del data['pids']
    del data['maxTreNum']
    del data['minTreNum']

    tables = []
    columns = []

    x = check_tables_and_columns(data)
    if x:
        print(x)
        tables = x[0]
        columns = x[1]
        return Export3(pids, treNums, tables, columns).work()
    else:
        print('接收的表名或者字段名存在错误')


# 检查json中的表名和字段名是否正确.
# 若正确返回tables,columns两个数组，若不正确返回None
def check_tables_and_columns(data):
    flag = True
    tables = []
    columns = []
    for key, value in data.items():
        obj_class_name = if_table_exist(key)
        if obj_class_name:
            tables.append(obj_class_name)
            if if_columns_exist(obj_class_name, value):
                columns.append(value)
            else:
                print('字段名不存在！')
                flag = False
                break
        else:
            print('表名不存在！')
            flag = False
            break

    if flag:
        return tables, columns
    else:
        return None


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
    obj = obj_class_name()
    for column in columns:
        export_header_map = getattr(obj_class_name, 'export_header_map')
        if not (column in export_header_map.keys()):
            flag = False
            break

    return flag
