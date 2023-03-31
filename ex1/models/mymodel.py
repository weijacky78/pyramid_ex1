from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .meta import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    key = Column(String(255), nullable=True, unique=True)
    menu_order = Column(Integer, nullable=False, default=0)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())


class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False, unique=True)
    description = Column(Text(255))
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())
    page_id = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    passHash = Column(String(255), nullable=False)
    cookieHash = Column(String(255), nullable=True)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())
