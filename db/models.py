from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True,nullable=False)
    image_url = Column(String,nullable=False)