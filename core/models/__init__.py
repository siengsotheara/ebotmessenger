from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2
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
        return Column(DATE, name='CREATE_AT', default=datetime.today)

    @declared_attr
    def create_by(cls):
        return Column(VARCHAR2(255), name='CREATE_BY', default='Dummy')

    @declared_attr
    def update_date(cls):
        return Column(DATE, name='UPDATE_AT')

    @declared_attr
    def update_by(cls):
        return Column(VARCHAR2(255), name='UPDATE_BY')

    @declared_attr
    def delete_date(cls):
        return Column(DATE, name='DELETE_AT')

    @declared_attr
    def delete_by(cls):
        return Column(VARCHAR2(255), name='DELETE_BY')

    @declared_attr
    def is_active(cls):
        return Column(VARCHAR2(1), name='IS_ACTIVE', nullable=False)

class User(Base, TrackMixin):
    __tablename__ = 'TBL_FACEBOOK_USER'
    id = Column(NUMBER, Sequence('TBL_USER_SEQ'), primary_key=True, name='ID')
    username = Column(VARCHAR(50), unique=True, name='USERNAME')
    password = Column(VARCHAR(50), name='PASSWORD')
    email = Column(VARCHAR(50), unique=True, name='EMAIL')
    facebook_id = Column(NUMBER, name='FACEBOOK_ID')

class BroadcastMessage(Base, TrackMixin):
    __tablename__ = 'TBL_FACEBOOK_BROADCAST_MSG'
    id = Column(NUMBER, Sequence('TBL_FACEBOOK_BROADCAST_MSG_SEQ'), primary_key=True, name='ID')
    message_creative_id = Column(NUMBER, name='MESSAGE_CREATIVE_ID')

class Attachment(Base, TrackMixin):
    __tablename__ = 'TBL_FACEBOOK_ATTACHMENT'
    id = Column(NUMBER, Sequence('TBL_FACEBOOK_ATTACHMENT_SEQ'), primary_key=True, name='ID')
    attachment_id = Column(NUMBER, name='ATTACHMENT_ID')

class FacebookConfig(Base):
    __tablename__ = 'TBL_FACEBOOK_CONFIG'
    code = Column(VARCHAR(100), name='CODE', primary_key=True)
    remark = Column(VARCHAR(200), name='REMARK')
    description = Column(VARCHAR(200), name='DESCRIPTION')


