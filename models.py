from sqlalchemy import Column,Integer,String,DateTime
from database import Base
import datetime

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    content = Column(String,index=True)
    created_at = Column(DateTime,index=True)
    updated_at = Column(DateTime,index=True)