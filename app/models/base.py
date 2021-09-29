import copy
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger, Date, event, DateTime, func, JSON
from contextlib import contextmanager

from app.libs.enums import ModuleStatus
from app.libs.error import Success
from app.libs.error_code import NotFound, SampleStatusError


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


class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_delete = Column(SmallInteger, server_default='0')

    modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
    query_reply = Column(JSON, comment='质疑和回复')
    module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')

    export_header_map = {}
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

    def submit(self):
        if self.module_status != ModuleStatus.UnSubmitted.value:
            return False
        with db.auto_commit():
            self.module_status = ModuleStatus.Submitted.value
        return True

    def finish(self):
        if self.module_status != ModuleStatus.Submitted.value:
            return False
        with db.auto_commit():
            self.module_status = ModuleStatus.Finished.value
        return True

    def record_modification(self, data):
        record = {'column': [], 'content': [], 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for key, value in data.items():
            record['column'].append(self.export_header_map.get(key))
            record['content'].append(value)
        with db.auto_commit():
            if self.modification is None:
                self.modification = []
            temp = copy.copy(self.modification)
            temp.append(record)
            self.modification = copy.copy(temp)

    # 将已提交的状态修改为未提交。在记录修改时调用，因为提交后每次修改都要把状态改为未提交。
    def cancel_submit(self):
        if self.module_status != ModuleStatus.Submitted.value:
            return False
        with db.auto_commit():
            self.module_status = ModuleStatus.UnSubmitted.value
        return True