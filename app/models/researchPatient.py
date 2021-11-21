from sqlalchemy import Column, Integer

from app.models import json2db_add
from app.models.base import Base, db
from app.spider.user_info import UserInfo


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
    def get_patients_by_research(cls, rid, user):
        uid = user.user_id
        scopes = user.scopes
        if 'CheckAllInResearch' in scopes:
            items = ResearchPatient.query.filter_by(rid=rid).all()
            pids = [item.pid for item in items]
        elif 'CheckCenterInResearch' in scopes:
            user_info = UserInfo().search_by_uid(uid).get('data')
            research_center_id = user_info['research_center_id']
            all_items = ResearchPatient.query.filter_by(rid=rid).all()
            all_pids = [item.pid for item in all_items]
            from app.models.base_line import Patient
            all_patients = Patient.query.filter(Patient.is_delete == 0,
                                                Patient.id.in_(all_pids)).all()
            pids = []
            for patient in all_patients:
                if patient.researchCenter == research_center_id:
                    pids.append(patient.id)
        else:
            all_items = ResearchPatient.query.filter_by(rid=rid).all()
            all_pids = [item.pid for item in all_items]
            from app.models.base_line import Patient
            all_patients = Patient.query.filter(Patient.is_delete == 0,
                                                Patient.id.in_(all_pids)).all()
            pids = []
            for patient in all_patients:
                if patient.account and uid in patient.account:
                    pids.append(patient.id)
        return pids
