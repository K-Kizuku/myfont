import os
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
HOST = os.environ.get('POSTGRES_HOST')

SQLALCHEMY_DETABASE_URL = "{}://{}:{}@{}/{}".format(
    DATABASE, USER, PASSWORD, HOST, DB_NAME
)
print(SQLALCHEMY_DETABASE_URL)
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
