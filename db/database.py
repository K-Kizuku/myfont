import os
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#DockerのDB設定
#herokuのdb設定
if os.environ.get('DATABASE_URL') == None:
    DATABASE = 'postgresql'
    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    DB_NAME = os.environ.get('POSTGRES_DB')
    HOST = os.environ.get('POSTGRES_HOST')

    SQLALCHEMY_DETABASE_URL = "{}://{}:{}@{}/{}".format(
        DATABASE, USER, PASSWORD, HOST, DB_NAME
    )
else: 
    SQLALCHEMY_DETABASE_URL = os.environ.get(
        'DATABASE_URL').replace('postgres://', 'postgresql://', 1)

engine = create_engine(
    SQLALCHEMY_DETABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
