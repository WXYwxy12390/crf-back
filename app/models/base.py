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


class ModificationAndDoubt:

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
    def question(self, data):
        data = copy.copy(data)
        data['doubt_column'] = self.export_header_map.get(data['doubt_column'])
        if self.module_status < ModuleStatus.Finished.value:
            return False
        from app.models import json2db_add
        from app.models.doubt import Doubt
        new_query = json2db_add(data, Doubt)
        with db.auto_commit():
            if self.doubt is None:
                self.doubt = []
            temp = copy.copy(self.doubt)
            temp.append(new_query.id)
            self.doubt = copy.copy(temp)
            # 修改状态
            from app.models.base_line import SpecimenInfo, DrugHistory
            from app.models.crf_info import FollInfo
            from app.models.other_inspect import ImageExams
            from app.models.cycle import Signs, SideEffect
            from app.models.therapy_record import DetailTrePlan

            if self.__class__ in [SpecimenInfo, FollInfo, DrugHistory]:
                item_ls = self.__class__.query.filter_by(pid=self.pid).all()
                for item in item_ls:
                    item.module_status = ModuleStatus.WithQuery.value
            elif self.__class__ in [ImageExams, Signs, SideEffect, DetailTrePlan]:
                item_ls = self.__class__.query.filter_by(pid=self.pid, treNum=self.treNum).all()
                for item in item_ls:
                    item.module_status = ModuleStatus.WithQuery.value
            else:
                self.module_status = ModuleStatus.WithQuery.value

        # 有的表和别的表属于同一模块。修改同一模块中其他表的状态。
        from app.models.therapy_record import OneToFive, Radiotherapy, Surgery, DetailTrePlan
        if self.__class__ in [OneToFive, Radiotherapy, Surgery]:
            detail_tre_plans = DetailTrePlan.query.filter_by(pid=self.pid, treNum=self.treNum).all()
            with db.auto_commit():
                for detail_tre_plan in detail_tre_plans:
                    detail_tre_plan.module_status = ModuleStatus.WithQuery.value
        from app.models.base_line import PastHis, DrugHistory
        if self.__class__ == PastHis:
            drugHistory_ls = DrugHistory.query.filter_by(pid=self.pid).all()
            with db.auto_commit():
                for drugHistory in drugHistory_ls:
                    drugHistory.module_status = ModuleStatus.WithQuery.value
        if self.__class__ == DetailTrePlan:
            one_to_five = OneToFive.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            surgery = Surgery.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            with db.auto_commit():
                if one_to_five:
                    one_to_five.module_status = ModuleStatus.WithQuery.value
                if surgery:
                    surgery.module_status = ModuleStatus.WithQuery.value
        if self.__class__ == DrugHistory:
            pastHis = PastHis.query.filter_by(pid=self.pid).first()
            with db.auto_commit():
                if pastHis:
                    pastHis.module_status = ModuleStatus.WithQuery.value
        return True

    def reply_doubt(self, doubt_id, data):
        if self.module_status != ModuleStatus.WithQuery.value:
            return False
        data['id'] = doubt_id
        data['is_replied'] = 1
        data['reply_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        from app.models import json2db
        from app.models.doubt import Doubt
        json2db(data, Doubt)

        # 求同模块内存在的所有质疑的id列表
        all_doubt_id = []
        from app.models.base_line import SpecimenInfo, DrugHistory
        from app.models.crf_info import FollInfo
        from app.models.other_inspect import ImageExams
        from app.models.cycle import Signs, SideEffect
        from app.models.therapy_record import DetailTrePlan
        if self.__class__ in [SpecimenInfo, FollInfo, DrugHistory]:
            item_ls = self.__class__.query.filter_by(pid=self.pid).all()
            for item in item_ls:
                if item.doubt:
                    all_doubt_id.extend(item.doubt)
        elif self.__class__ in [ImageExams, Signs, SideEffect, DetailTrePlan]:
            item_ls = self.__class__.query.filter_by(pid=self.pid, treNum=self.treNum).all()
            for item in item_ls:
                if item.doubt:
                    all_doubt_id.extend(item.doubt)
        else:
            all_doubt_id.extend(self.doubt)

        from app.models.therapy_record import OneToFive, Radiotherapy, Surgery
        if self.__class__ in [OneToFive, Radiotherapy, Surgery]:
            detail_tre_plans = DetailTrePlan.query.filter_by(pid=self.pid, treNum=self.treNum).all()
            for detail_tre_plan in detail_tre_plans:
                if detail_tre_plan.doubt:
                    all_doubt_id.extend(detail_tre_plan.doubt)
        from app.models.base_line import PastHis
        if self.__class__ == PastHis:
            drugHistory_ls = DrugHistory.query.filter_by(pid=self.pid).all()
            for drugHistory in drugHistory_ls:
                if drugHistory.doubt:
                    all_doubt_id.extend(drugHistory.doubt)
        if self.__class__ == DetailTrePlan:
            one_to_five = OneToFive.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            surgery = Surgery.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            if one_to_five and one_to_five.doubt:
                all_doubt_id.extend(one_to_five.doubt)
            if surgery and surgery.doubt:
                all_doubt_id.extend(surgery.doubt)
        if self.__class__ == DrugHistory:
            pastHis = PastHis.query.filter_by(pid=self.pid).first()
            if pastHis and pastHis.doubt:
                all_doubt_id.extend(pastHis.doubt)

        # 检查是否还存在没有回复的质疑，若存在则不修改状态
        doubt_ls = Doubt.query.filter(Doubt.is_delete == 0, Doubt.id.in_(all_doubt_id)).all()
        for doubt in doubt_ls:
            if doubt.is_replied == 0:
                return True

        with db.auto_commit():
            # 修改状态
            if self.__class__ in [SpecimenInfo, FollInfo, DrugHistory]:
                item_ls = self.__class__.query.filter_by(pid=self.pid).all()
                for item in item_ls:
                    item.module_status = ModuleStatus.AllReplied.value
            elif self.__class__ in [ImageExams, Signs, SideEffect, DetailTrePlan]:
                item_ls = self.__class__.query.filter_by(pid=self.pid, treNum=self.treNum).all()
                for item in item_ls:
                    item.module_status = ModuleStatus.AllReplied.value
            else:
                self.module_status = ModuleStatus.AllReplied.value

        # 有的表和别的表属于同一模块。修改同一模块中其他表的状态。
        if self.__class__ in [OneToFive, Radiotherapy, Surgery]:
            detail_tre_plans = DetailTrePlan.query.filter_by(pid=self.pid, treNum=self.treNum).all()
            with db.auto_commit():
                for detail_tre_plan in detail_tre_plans:
                    detail_tre_plan.module_status = ModuleStatus.AllReplied.value
        from app.models.base_line import PastHis
        if self.__class__ == PastHis:
            drugHistory_ls = DrugHistory.query.filter_by(pid=self.pid).all()
            with db.auto_commit():
                for drugHistory in drugHistory_ls:
                    drugHistory.module_status = ModuleStatus.AllReplied.value
        if self.__class__ == DetailTrePlan:
            one_to_five = OneToFive.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            surgery = Surgery.query.filter_by(pid=self.pid, treNum=self.treNum).first()
            with db.auto_commit():
                if one_to_five:
                    one_to_five.module_status = ModuleStatus.AllReplied.value
                if surgery:
                    surgery.module_status = ModuleStatus.AllReplied.value
        if self.__class__ == DrugHistory:
            pastHis = PastHis.query.filter_by(pid=self.pid).first()
            with db.auto_commit():
                if pastHis:
                    pastHis.module_status = ModuleStatus.AllReplied.value
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
