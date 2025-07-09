from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Boolean, Float, func,Date
from app.db.initdb import AsyncBase
class User(AsyncBase):
    '''Роли Суперадмин, Руководитель'''
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chat_id = Column(BigInteger, nullable=False)
    username = Column(String(256))
    role = Column(String(256), nullable=False)
    full_name = Column(String(256))
    phone = Column(String(256))


