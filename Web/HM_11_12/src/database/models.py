from sqlalchemy import Column, Integer, String, ForeignKey, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date, DateTime

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
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
