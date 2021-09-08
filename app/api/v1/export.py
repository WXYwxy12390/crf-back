from flask import request
from app.libs.redprint import Redprint
from app.utils.export import Export

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
    treIndexes = data['treNums'] if 'treNums' in keys else []
    follInfoNum = data['follInfoNum'] if 'follInfoNum' in keys else 0
    baseLine = []
    trementInfo = []
    follInfo = {}
    baseLine_error_info = ''
    trementInfo_error_info = ''
    follInfo_error_info = ''
    if 'baseLine' in keys:
        baseLine = data['baseLine']
        baseLine_error_info = check_tables_and_columns(baseLine)
    if 'trementInfo' in keys:
        trementInfo = data['trementInfo']
        trementInfo_error_info = check_tables_and_columns(trementInfo)
    if 'follInfo' in keys:
        follInfo = data['follInfo']
        if_table_right = if_table_exist(follInfo['table'])
        if if_table_right:
            error_columns = if_columns_exist(if_table_right, follInfo['column'])
            if error_columns:
                follInfo_error_info += '随访信息错误的字段名名：' + str(error_columns)
        else:
            follInfo_error_info += '随访信息表名错误'

    if not (baseLine_error_info or trementInfo_error_info or follInfo_error_info):
        return Export(pids, treIndexes, follInfoNum, baseLine, trementInfo, follInfo).work()
    else:
        return baseLine_error_info + '\n' + trementInfo_error_info + '\n' + follInfo_error_info


# 检查json中的表名和字段名是否正确.
# 若正确返回tables,columns两个数组，若不正确返回None
def check_tables_and_columns(data):
    error_info = ''
    for k in range(0, len(data)):
        table = data[k].get('table')
        column = data[k].get('column')
        obj_class_name = if_table_exist(table)
        if obj_class_name:
            data[k]['table'] = obj_class_name
            error_columns = if_columns_exist(obj_class_name, column)
            if error_columns:
                error_info += table + '表中错误的字段名：' + str(error_columns)
                break
        else:
            error_info += '错误的表名：' + table
            break
    return error_info


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
    error_columns = []
    export_header_map = getattr(obj_class_name, 'export_header_map')
    keys = export_header_map.keys()
    for column in columns:
        if not (column in keys):
            error_columns.append(column)
    return error_columns
