from email.policy import default
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from uuid import uuid4

Base = declarative_base()

def generate_uuid():
    return str(uuid4())

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer,primary_key=True,default=generate_uuid)
    email = Column(String, unique=True,nullable=False)
    image_url = Column(String,nullable=False)