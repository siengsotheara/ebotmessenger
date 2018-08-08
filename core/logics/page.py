from core.logics.base import *
from core.models import FacebookConfig
from sqlalchemy import subquery



class PageLogic(LogicBase):
    def __init__(self):
        self.__classname__ = FacebookConfig

    def _findByKey(self, key):
        q = db.query(self.__classname__).filter(self.__classname__.key == key).first()
        return q
pages = PageLogic()