import copy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, DateTime, func
from contextlib import contextmanager

from sqlalchemy.orm.attributes import flag_modified

from app.libs.enums import ModuleStatus
from app.libs.error_code import NotFound


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

    # 对某访视的某模块中某字段提出质疑
    def question(self, data, pid, treNum):
        flag = False
        treNum_str = str(treNum)
        from app.models.base_line import Patient
        patient = Patient.query.get_or_404(pid)
        module = self.__class__.__name__
        print(module)
        module_status = copy.copy(patient.module_status)
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
        index = len(data)
        data['doubt_column_cn'] = self.export_header_map.get(data['doubt_column'])  # 该字段的中文
        data['is_replied'] = 0
        data['doubt_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['index'] = index  # 表示每一个质疑在质疑列表中的索引号。用于在所有质疑中定位到某索引。
        if doubt is None:
            doubt = []
        doubt.append(data)
        with db.auto_commit():
            self.doubt = doubt
            flag_modified(patient, 'doubt')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag

    def reply_doubt(self, data, pid, treNum, doubt_index):
        flag = False
        treNum_str = str(treNum)
        from app.models.base_line import Patient
        patient = Patient.query.get_or_404(pid)
        module = self.__class__.__name__
        print(module)
        module_status = copy.copy(patient.module_status)
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
        all_doubt[doubt_index]['reply_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with db.auto_commit():
            self.doubt = all_doubt
            flag_modified(patient, 'doubt')  # 加上这句JSON类型数据才可以更新到数据库。原因不明。
        return flag

    def record_modification(self, data, pid, treNum):
        flag = False  # 标记是否成功记录下修改
        treNum_str = str(treNum)
        from app.models.base_line import Patient
        patient = Patient.query.get_or_404(pid)
        module = self.__class__.__name__
        module_status = patient.module_status
        if module_status.get(module) is None:
            return flag
        if module_status[module].get(treNum_str) is None or \
                module_status[module].get(treNum_str) == ModuleStatus.UnSubmitted.value:
            return flag

        flag = True
        '''
        参数data结构应该是
        {
            'column':'',    修改的字段
            'content':''    修改的内容
        }
        现在要补充上修改的时间和修改字段的中文
        '''
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
        return flag


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
