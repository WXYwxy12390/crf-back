import copy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger, Date, DateTime, func, JSON
from contextlib import contextmanager
from app.libs.enums import ModuleStatus
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


# class ModificationAndDoubt:
#     modification = Column(JSON, comment='溯源功能。记录提交后的修改记录')
#     doubt = Column(JSON, comment='质疑和回复')
#     module_status = Column(Integer, server_default='0', comment='该模块的状态，0未提交，1已提交，2已结束，3有质疑，4已回复')
#
#     def submit(self):
#         if self.module_status != ModuleStatus.UnSubmitted.value:
#             return False
#         with db.auto_commit():
#             self.module_status = ModuleStatus.Submitted.value
#         return True
#
#     def finish(self):
#         if self.module_status != ModuleStatus.Submitted.value:
#             return False
#         with db.auto_commit():
#             self.module_status = ModuleStatus.Finished.value
#         return True
#
#     # 对某访视的某模块中某字段提出质疑
#     def doubt(self, data):
#         data = copy.copy(data)
#         data['doubt_column'] = self.export_header_map.get(data['doubt_column'])
#         if self.module_status < ModuleStatus.Finished.value:
#             return False
#         from app.models import json2db_add
#         from app.models.doubt import Doubt
#         new_query = json2db_add(data, Doubt)
#         with db.auto_commit():
#             if self.doubt is None:
#                 self.doubt = []
#             temp = copy.copy(self.doubt)
#             temp.append(new_query.id)
#             self.doubt = copy.copy(temp)
#             self.module_status = ModuleStatus.WithQuery.value
#         return True
#
#     def reply(self, id, data):
#         if self.module_status != ModuleStatus.WithQuery.value:
#             return False
#         data['id'] = id
#         data['is_replied'] = 1
#         data['reply_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         from app.models import json2db
#         from app.models.doubt import Doubt
#         json2db(data, Doubt)
#         doubt_ls = Doubt.query.filter(Doubt.is_delete == 0, Doubt.id.in_(self.query_reply)).all()
#
#         # 检查是否还存在质疑，若不存在则状态改为已全部恢复
#         for doubt in doubt_ls:
#             if doubt.is_replied == 0:
#                 return True
#         with db.auto_commit():
#             self.module_status = ModuleStatus.AllReplied.value
#         return True
#
#     def record_modification(self, data):
#         record = {'column': [], 'content': [], 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#         for key, value in data.items():
#             record['column'].append(self.export_header_map.get(key))
#             record['content'].append(value)
#         with db.auto_commit():
#             if self.modification is None:
#                 self.modification = []
#             temp = copy.copy(self.modification)
#             temp.append(record)
#             self.modification = copy.copy(temp)
#
#     # 将已提交的状态修改为未提交。在记录修改时调用，因为提交后每次修改都要把状态改为未提交。
#     def cancel_submit(self):
#         if self.module_status != ModuleStatus.Submitted.value:
#             return False
#         with db.auto_commit():
#             self.module_status = ModuleStatus.UnSubmitted.value
#         return True


class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_delete = Column(SmallInteger, server_default='0')

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

    # 对某访视的某模块中某字段提出质疑
    def doubt(self, data):
        data = copy.copy(data)
        data['doubt_column'] = self.export_header_map.get(data['doubt_column'])
        if self.module_status < ModuleStatus.Finished.value:
            return False
        from app.models import json2db_add
        from app.models.doubt import Doubt
        new_query = json2db_add(data, Doubt)
        with db.auto_commit():
            if self.query_reply is None:
                self.query_reply = []
            temp = copy.copy(self.query_reply)
            temp.append(new_query.id)
            self.query_reply = copy.copy(temp)
            self.module_status = ModuleStatus.WithQuery.value
        return True

    def reply(self, id, data):
        if self.module_status != ModuleStatus.WithQuery.value:
            return False
        data['id'] = id
        data['is_replied'] = 1
        data['reply_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        from app.models import json2db
        from app.models.doubt import Doubt
        json2db(data, Doubt)
        doubt_ls = Doubt.query.filter(Doubt.is_delete == 0, Doubt.id.in_(self.query_reply)).all()

        # 检查是否还存在质疑，若不存在则状态改为已全部恢复
        for doubt in doubt_ls:
            if doubt.is_replied == 0:
                return True
        with db.auto_commit():
            self.module_status = ModuleStatus.AllReplied.value
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
