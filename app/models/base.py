


from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger, Date, event, DateTime, func
from contextlib import contextmanager

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

class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime,server_default=func.now())
    update_time = Column(DateTime,server_default=func.now(),onupdate=func.now())
    is_delete = Column(SmallInteger, server_default='0')
    # record_date = Column(Date)
    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())
    #对象转换为字典，要重写的2个方法，可以提取一个到基类
    def __getitem__(self, item):
        return  getattr(self,item)

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
    #假删除
    def delete(self):
        self.is_delete = 1

    @staticmethod
    def on_created():
        pass

    # def update_sample_time(self):
    #     if hasattr(self,'sample_id'):
    #         sample = Sample.query.get_or_404(self.sample_id)
    #     elif hasattr(self,'cycle_id'):
    #         cycle = Cycle.query.get_or_404(self.cycle_id)
    #         sample = Sample.query.get_or_404(self.sample_id)
    #     sample.update_time = func.now()
