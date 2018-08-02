from core.logics.base import *
from core.models import BroadcastMessage
from sqlalchemy import subquery



class BroadcastMesseageLogic(LogicBase):
    def __init__(self):
        self.__classname__ = BroadcastMessage

    def _search(self, **kwargs):
        q = self._active()
        q = q.order_by(self.__classname__.create_at.desc())
        return q
broadcastmessages = BroadcastMesseageLogic()