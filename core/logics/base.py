from core.databases import db
from core.models.enum import Status
from sqlalchemy import func, desc, asc, and_, or_ , not_
from datetime import datetime

class LogicBase:
    __classname__ = None;

    def __init__(self, *args, **kwargs):
        self.__classname__ = kwargs['__classname__']

    def _new(self):
        result = self.__classname__()
        return result

    def _all(self):
        result = db.query(self.__classname__)
        if result.count():
            if hasattr(result[0], "is_active"):
                result = result.filter_by(is_active=True)
        return result.all()

    def _active(self):
        q = db.query(self.__classname__).filter_by(is_active=True)
        return q

    def _search(self, **kwargs):
        search = kwargs['search'] if 'search' in kwargs else ''
        q = self._active()
        if search:
            if hasattr(self.__classname__, 'name') and hasattr(self.__classname__, 'code'):
                q = q.filter(
                    or_(func.lower(self.__classname__.code).like('%'+search.lower()+'%'),
                        func.lower(self.__classname__.name).like('%'+search.lower()+'%')
                        )
                    )
            elif hasattr(self.__classname__, 'code'):
                q = q.filter(func.lower(self.__classname__.code).like('%'+search.lower()+'%'))
            elif hasattr(self.__classname__, 'name'):
                q = q.filter(func.lower(self.__classname__.name).like('%'+search.lower()+'%'))
        return q

    def _find(self, id, update=False):
        result = db.query(self.__classname__).filter_by(id=id).first()
        return result

    def _count(self):
        return self._active().count()

    def _insert(self, obj):
        if hasattr(obj, 'is_active'):
            obj.is_active=Status.Y

        db.add(obj)
        db.commit()

    def _update(self, obj):
        if hasattr(obj, 'update_at'):
            obj.update_date=datetime.date.today()
        if hasattr(obj, 'update_by'):
            obj.update_by = 'Default Update'

        db.commit()

    def _delete(self, obj):
        if hasattr(obj, 'delete_by'):
            obj.delete_by = 'Default Delete'
        if hasattr(obj, 'delete_at'):
            obj.delete_date = datetime.date.today()
        if hasattr(obj, 'is_active'):
            obj.is_active=Status.N
        else:
            db.remove(obj)

        db.commit()
