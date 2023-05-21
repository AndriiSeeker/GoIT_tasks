import os
import pathlib
import configparser

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
domain = os.environ.get('POSTGRES_DOMAIN')
port = os.environ.get('POSTGRES_PORT')
db_name = os.environ.get('POSTGRES_DB_NAME')

SQLALCHEMY_DB_URL = os.environ.get('SQLALCHEMY_DB')

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()