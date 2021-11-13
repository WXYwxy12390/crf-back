from sqlalchemy import Column, Integer, String

from app.models.base import Base, db

# 研究。可以将任意中心的样本放入一个研究中
from app.models.researchPatient import ResearchPatient
from app.models.researchUser import ResearchUser


class Research(Base):
    __tablename__ = 'research'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, comment='研究的名称')
    description = Column(String(255), comment='研究的描述')

    def keys(self):
        return ['id', 'name', 'description']

    @classmethod
    def get_by_name(cls, name):
        if name is None:
            return None
        item = Research.query.filter_by(name=name).first()
        return item

    def delete(self):
        research_patient_list = ResearchPatient.query.filter_by(rid=self.id).all()
        research_user_list = ResearchUser.query.filter_by(rid=self.id).all()

        with db.auto_commit():
            for item in research_patient_list:
                item.delete()
            for item in research_user_list:
                item.delete()
            self.is_delete = 1


