from core.logics.base import *
from core.models import BroadcastMessage
from sqlalchemy import subquery



class BroadcastLogic(LogicBase):
    def __init__(self):
        self.__classname__ = BroadcastMessage

broadcast = BroadcastLogic()