import datetime

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class Archive(base):
    __tablename__ = 'archives'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    aec = Column(String, nullable=False, unique=True, primary_key=True)
    adres_ip = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    is_activ = Column(Boolean, default=0)


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    aet = Column(String)
    adres_ip = Column(String)
    port = Column(Integer)
    include_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_activ = Column(Boolean, default=0)
    archive = relationship("Archive")


class ImageNNProcessing(base):
    __tablename__ = 'nn_processing'
    id = Column(Integer, nullable=False, primary_key=True)
    study_id = Column(String, unique=True, nullable=False)
    filepath_before = Column(String, nullable=True, unique=False)
    filepath_after = Column(String, nullable=True, unique=True)
    user_upload = Column(Integer, ForeignKey('users.id'))
    date_upload = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    state = Column(String, nullable=False)


class Session(base):
    __tablename__ = 'user_session'
    id = Column(Integer, nullable=False, primary_key=True)
    start_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
