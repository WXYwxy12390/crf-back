from sqlalchemy import Column, Integer

from app.models.base import Base


class ResearchUser(Base):
    __tablename__ = 'research_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, comment='用户id。RBAC库中user表中的id')
    rid = Column(Integer, comment='研究id。research表中的id')

    def keys(self):
        return ['id', 'uid', 'rid']

    # 判断某用户是否参与了某研究
    @classmethod
    def if_user_in_research(cls, uid, rid):
        item = ResearchUser.query.filter_by(uid=uid, rid=rid).first()
        if item is None:
            return False
        else:
            return True
