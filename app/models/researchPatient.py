from sqlalchemy import Column, Integer

from app.models import json2db_add
from app.models.base import Base, db


class ResearchPatient(Base):
    __tablename__ = 'research_patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id。patient表中的id')
    rid = Column(Integer, comment='研究id。research表中的id')

    def keys(self):
        return ['id', 'pid', 'rid']

    @classmethod
    def add_patients_to_research(cls, rid, pids):
        for pid in pids:
            item = ResearchPatient.query.filter_by(rid=rid, pid=pid).first()
            if item is None:
                json2db_add({'pid': pid, 'rid': rid}, ResearchPatient)

    @classmethod
    def remove_patients_from_research(cls, rid, pids):
        for pid in pids:
            item = ResearchPatient.query.filter_by(rid=rid, pid=pid).first()
            if item is not None:
                with db.auto_commit():
                    item.delete()

    @classmethod
    def get_patients_by_research(cls, rid):
        items = ResearchPatient.query.filter_by(rid=rid).all()
        pids = [item.pid for item in items]
        return pids

    @classmethod
    def get_researches_by_patient(cls, pid):
        items = ResearchPatient.query.filter_by(pid=pid).all()
        rids = [item.rid for item in items]
        return rids
