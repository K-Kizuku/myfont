from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

def generate_uuid():
    return str(uuid4())

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String,primary_key=True,default=generate_uuid)
    email = Column(String, unique=True,nullable=False)
    password_hash = Column(String)
    images = relationship("Image")

class Image(Base):
    __tablename__ = "images"
    image_id = Column(String,primary_key=True, default=generate_uuid)
    character = Column(String, nullable=False)
    image_url = Column(String, unique=True, nullable=False)
    user_id = Column(ForeignKey("users.user_id"))