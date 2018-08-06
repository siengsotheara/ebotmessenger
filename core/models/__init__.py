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
    def create_at(cls):
        return Column(DATE, name='CREATE_AT', default=datetime.today)

    @declared_attr
    def create_by(cls):
        return Column(VARCHAR2(255), name='CREATE_BY')

    @declared_attr
    def update_at(cls):
        return Column(DATE, name='UPDATE_AT', onupdate=datetime.today)

    @declared_attr
    def update_by(cls):
        return Column(VARCHAR2(255), name='UPDATE_BY')

    @declared_attr
    def delete_at(cls):
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
    is_login_ad = Column(VARCHAR(1), name='IS_LOGIN_AD')
    email = Column(VARCHAR(50), unique=True, name='EMAIL')
    facebook_id = Column(VARCHAR(50), name='FACEBOOK_ID')

class BroadcastMessage(Base, TrackMixin):
    __tablename__ = 'TBL_FACEBOOK_BROADCAST_MSG'
    id = Column(NUMBER, Sequence('TBL_FACEBOOK_BROADCAST_MSG_SEQ'), primary_key=True, name='ID')
    message_creative_id = Column(VARCHAR(50), name='MESSAGE_CREATIVE_ID')
    message_creative_type =  Column(VARCHAR(50), name='MESSAGE_CREATIVE_TYPE')
    is_already_broadcast = Column(VARCHAR(1), name='IS_ALREADY_BROADCAST')
        
class Broadcast(Base, TrackMixin):
    __tablename__ = 'TBL_FACEBOOK_BROADCAST'
    id =  Column(NUMBER, Sequence('TBL_FACEBOOK_BROADCAST_SEQ'), primary_key=True, name='ID')
    message_creative_id = Column(VARCHAR(50), name='MESSAGE_CREATIVE_ID')
    notification_type = Column(VARCHAR(50), name='NOTIFICATION_TYPE')
    broadcast_id = Column(VARCHAR(50), name='BROADCAST_ID')
    messaging_type = Column(VARCHAR(50), name='MESSAGING_TYPE')
    tag = Column(VARCHAR(50), name='TAG')

class FacebookConfig(Base):
    __tablename__ = 'TBL_FACEBOOK_CONFIG'
    key = Column(VARCHAR(100), name='KEY', primary_key=True)
    value = Column(VARCHAR(200), name='VALUE')
    description = Column(VARCHAR(200), name='DESCRIPTION')


