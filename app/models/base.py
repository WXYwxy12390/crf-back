import copy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, DateTime, func
from contextlib import contextmanager

from sqlalchemy.orm.attributes import flag_modified

from app.libs.enums import ModuleStatus
from app.libs.error_code import NotFound
from app.utils.modification import if_status_allow_modification, get_module_by_class_name


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'is_delete' not in kwargs.keys():
            kwargs['is_delete'] = 0
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        elif rv.is_delete == 1:
            raise NotFound(msg='该资源已删除', error_code=10021)
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class ModificationAndDoubt:
    '''
    该方法用于对某访视的某模块中某字段提出质疑。
    参数data的结构为
    {
        'doubt_column':'',  质疑的字段
        'doubt_description':''  质疑的描述
    }
    每个质疑存入数据库的结构为
    {
        'doubt_column':'',  质疑的字段
        'doubt_column_cn',  质疑的字段的中文
        'doubt_description':''  质疑的描述
        'is_replied':0,    是否已经回复，0表示未回复，1表示已回复
        'doubt_time':  ,    质疑的时间
        'index':  ,     该质疑在质疑列表中的索引号
    }
    '''

    def question(self, data, pid, treNum):
        flag = False
        treNum_str = str(treNum)
        from app.models.base_line import Patient
        patient = Patient.query.get_or_404(pid)
        module = get_module_by_class_name(self.__class__.__name__)

        module_status = copy.copy(patient.module_status)
        if not module_status or not module_status.get(module) or not module_status[module].get(treNum_str):
            return flag
        if module_status[module][treNum_str] not in [ModuleStatus.CRAMonitoring.value,
                                                     ModuleStatus.CRADoubt.value, ModuleStatus.WithReply.value]:
            return flag

        flag = True
        if module_status[module][treNum_str] == ModuleStatus.CRAMonitoring.value:
            module_status[module][treNum_str] = ModuleStatus.CRADoubt.value
            with db.auto_commit():
                patient.module_status = module_status
                flag_modified(patient, 'module_status')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。

        data = copy.copy(data)
        doubt = copy.copy(self.doubt)
        if doubt is None:
            doubt = []
        index = len(doubt)
        data['doubt_column_cn'] = self.export_header_map.get(data['doubt_column'])  # 该字段的中文
        data['is_replied'] = 0
        data['doubt_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['index'] = index  # 表示每一个质疑在质疑列表中的索引号。用于在所有质疑中定位到某索引。

        doubt.append(data)
        with db.auto_commit():
            self.doubt = doubt
            flag_modified(self, 'doubt')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag

    '''
    该方法用于对某个质疑回复。
    data结构为{ 'reply':'' ]
    通过doubt_index定位到要回复的质疑，并添加回复的内容和回复的时间
    回复后，该质疑的结构为
    {
        'doubt_column':'',  质疑的字段
        'doubt_column_cn',  质疑的字段的中文
        'doubt_description':''  质疑的描述
        'is_replied':1,    是否已经回复，0表示未回复，1表示已回复
        'doubt_time':  ,    质疑的时间
        'index':  ,     该质疑在质疑列表中的索引号
        'reply':'',     回复的内容
        'reply_time':   回复的时间
    }
    '''

    def reply_doubt(self, data, pid, treNum, doubt_index):
        flag = False
        treNum_str = str(treNum)
        from app.models.base_line import Patient
        patient = Patient.query.get_or_404(pid)
        module = get_module_by_class_name(self.__class__.__name__)

        module_status = copy.copy(patient.module_status)
        if not module_status or not module_status.get(module) or not module_status[module].get(treNum_str):
            return flag
        if module_status[module][treNum_str] not in [ModuleStatus.CRADoubt.value, ModuleStatus.WithReply.value]:
            return flag

        flag = True
        if module_status[module][treNum_str] == ModuleStatus.CRADoubt.value:
            module_status[module][treNum_str] = ModuleStatus.WithReply.value
            with db.auto_commit():
                patient.module_status = module_status
                flag_modified(patient, 'module_status')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。

        data = copy.copy(data)
        all_doubt = copy.copy(self.doubt)
        all_doubt[doubt_index]['reply'] = data['reply']
        all_doubt[doubt_index]['is_replied'] = 1
        all_doubt[doubt_index]['reply_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with db.auto_commit():
            self.doubt = all_doubt
            flag_modified(self, 'doubt')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag

    '''
    该方法用于记录修改。
    参数data结构应该是
    {
        'column':'',    修改的字段
        'content':'',   修改的内容
        'description:'' 修改的描述
    }
    在方法中要补充上修改的时间,修改字段的中文，然后存入数据库。
    '''

    def record_modification(self, data):
        data = copy.copy(data)
        data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['column_cn'] = self.export_header_map.get(data['column'])
        modification = copy.copy(self.modification)
        if modification is None:
            modification = []
        modification.append(data)
        with db.auto_commit():
            self.modification = modification
            flag_modified(self, 'modification')

    # 将修改记录和质疑按时间顺序放在一个列表中。若质疑已被回复，则以回复的时间为准。
    def get_history(self):
        history = []
        modification = copy.copy(self.modification)
        doubt = copy.copy(self.doubt)
        history.extend(modification)
        history.extend(doubt)
        history_length = len(history)

        def get_time(dic):
            if dic.get('time') is not None:
                time = dic['time']
            elif dic['is_replied'] == 1:
                time = dic['reply_time']
            else:
                time = dic['doubt_time']
            return time

        for i in range(0, history_length):
            max_index = i
            for j in range(i + 1, history_length):
                if get_time(history[j]) > get_time(history[max_index]):
                    max_index = j
            temp = copy.copy(history[max_index])
            history[max_index] = copy.copy(history[i])
            history[i] = temp
        return history


class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_delete = Column(SmallInteger, server_default='0')

    # 和导出功能有关
    header_num = 0

    # record_date = Column(Date)
    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())
    # 对象转换为字典，要重写的2个方法，可以提取一个到基类
    def __getitem__(self, item):
        return getattr(self, item)

    # @property
    # def create_datetime(self):
    #     if self.create_time:
    #         return datetime.fromtimestamp(self.create_time)
    #     else:
    #         return None
    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # 假删除
    def delete(self):
        self.is_delete = 1

    # 和导出功能有关
    # 既能过滤空数据，也能过滤对象是空对象的情况
    def filter_none(self, data, item=None):
        if data is None:
            return '/'
        if item:
            val = getattr(data, item)
        else:
            val = data
        if val is not None and val != '' and val != [] and val != {}:
            return val
        else:
            return '/'

    # 和导出功能有关
    def change_bool_to_yes_or_no(self, bool_value):
        if bool_value is None:
            return '/'
        return '是' if bool_value else '否'

    # 和导出功能有关
    def format_radio_data(self, object, item):
        if object is None:
            return '/'
        data = getattr(object, item)
        if data is None:
            return '/'
        radio = data.get('radio')
        other = data.get('other')
        value = ",".join(radio)
        if other:
            value = value + "," + "其他: " + other
        return value
