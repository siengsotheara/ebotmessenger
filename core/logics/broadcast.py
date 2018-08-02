from core.logics.base import *
from core.models import Broadcast
from sqlalchemy import subquery



class BroadcastLogic(LogicBase):
    def __init__(self):
        self.__classname__ = Broadcast

    def _search(self, **kwargs):
        q = self._active()
        q = q.order_by(self.__classname__.id.desc())
        return q

broadcasts = BroadcastLogic()