from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date
base = declarative_base()


class Contact(base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(80))
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(100))
    birth = Column(Date)
    description = Column(String, default="")
