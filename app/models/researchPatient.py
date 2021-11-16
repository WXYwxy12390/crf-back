from sqlalchemy import Column, Integer

from app.models import json2db_add
from app.models.base import Base, db


class ResearchPatient(Base):
    __tablename__ = 'research_patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id。patient表中的id')
    rid = Column(Integer, comment='研究id。research表中的id')
    uid = Column(Integer, comment='加入该病人至该研究的用户id')

    def keys(self):
        return ['id', 'pid', 'rid', 'uid']

    @classmethod
    def add_patients_to_research(cls, rid, pids, uid):
        for pid in pids:
            item = ResearchPatient.query.filter_by(rid=rid, pid=pid).first()
            if item is None:
                json2db_add({'pid': pid, 'rid': rid, 'uid': uid}, ResearchPatient)

    @classmethod
    def remove_patients_from_research(cls, rid, pids):
        for pid in pids:
            item = ResearchPatient.query.filter_by(rid=rid, pid=pid).first()
            if item is not None:
                with db.auto_commit():
                    item.delete()

    @classmethod
    def get_patients_by_research(cls, rid, user):
        uid = user.user_id
        scopes = user.scopes
        if 'CheckAllInResearch' in scopes:
            items = ResearchPatient.query.filter_by(rid=rid).all()
        else:
            items = ResearchPatient.query.filter_by(rid=rid, uid=uid).all()
        pids = [item.pid for item in items]
        return pids


    @classmethod
    def get_researches_by_patient(cls, pid):
        items = ResearchPatient.query.filter_by(pid=pid).all()
        rids = [item.rid for item in items]
        return rids
