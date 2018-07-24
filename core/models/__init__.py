from sqlalchemy import Column, Integer, BigInteger, String, Sequence, Numeric, DateTime,  Date, Boolean, Binary, Text, Unicode, UnicodeText, Time
from sqlalchemy import ForeignKey
from sqlalchemy import event, DDL, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.sql.schema import MetaData

from sqlalchemy.ext.declarative import declarative_base, declared_attr, as_declarative
from flask import session, request, g
from datetime import datetime, timedelta

from core.databases import db
from core.models import enum


Base = declarative_base()

class TrackMixin(object):
    """The TrackMixin Tables is wholed the default tracking columns to tables inherit from this class Model"""
    @declared_attr
    def create_date(cls):
        return Column(DateTime, default=datetime.utcnow, server_default=func.now())

    @declared_attr
    def create_by(cls):
        return Column(String(50), default=u'Dummy', server_default='Dummy')

    @declared_attr
    def update_date(cls):
        return Column(DateTime, onupdate=datetime.utcnow)

    @declared_attr
    def update_by(cls):
        return Column(String(50), onupdate=u'Dummy')

    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True, server_default='t')

#class Atm(Base, TrackMixin):
#    __tablename__ = 'atm'
#    id = Column(Integer, primary_key=True)
#    x = Column(float)
#    y = Column(float)

#class User(Base, TrackMixin):
#    __tablename__ = 'user'
#    id = Column(Integer, primary_key=True)
#    username = Column(String(50), unique=True, index=True, nullable=False)

#    pitches = relationship('Pitch', primaryjoin='foreign(PitchMergeDetail.pitch_id) == remote(Pitch.id)')


class BroadcastMessage(Base, TrackMixin):
    __tablename__ = 'TBL_BROADCAST_MESSAGE'
    id = Column(Numeric, name='ID',primary_key=True)
    message_creative_id = Column(Integer, name='MESSAGE_CREATIVE_ID')

