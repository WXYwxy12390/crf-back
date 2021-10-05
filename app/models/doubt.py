from sqlalchemy import Column, Integer, String, SmallInteger, DateTime

from app.models.base import Base


class Doubt(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='质疑id')
    doubt_column = Column(String(255), comment='被质疑的字段')
    doubt_description = Column(String(1000), comment='被质疑的字段')
    is_replied = Column(SmallInteger, server_default='0', comment='是否被回复')
    reply = Column(String(1000), comment='回复内容')
    reply_time = Column(DateTime, comment='回复的时间')
