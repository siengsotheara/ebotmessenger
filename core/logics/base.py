from core.databases import db
from core.models.enum import Status

from sqlalchemy import func, desc, asc, and_, or_ , not_
from datetime import datetime

from flask import session

class LogicBase:
    __classname__ = None;

    #def __init__(self, *args, **kwargs):
    #    self.__classname__ = kwargs['__classname__']

    def _new(self):
        result = self.__classname__()
        return result

    def _all(self):
        result = db.query(self.__classname__)
        if result.count():
            if hasattr(result[0], "is_active"):
                result = result.filter_by(is_active=Status.Y)
        return result.all()

    def _active(self):
        if hasattr(self.__classname__, 'is_active'):
            q = db.query(self.__classname__).filter_by(is_active=Status.Y)
            return q
        else:
            return db.query(self.__classname__)

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
        if hasattr(obj, 'create_by'):
            obj.create_by = self._current_username()

        db.add(obj)
        db.commit()

    def _update(self, obj):
        if hasattr(obj, 'update_at'):
            obj.update_at = datetime.utcnow()
        if hasattr(obj, 'update_by'):
            obj.update_by = self._current_username()
        
        db.commit()

    def _delete(self, obj):
        if hasattr(obj, 'delete_by'):
            obj.delete_by = self._current_username()
        if hasattr(obj, 'delete_at'):
            obj.delete_at = datetime.utcnow()
        if hasattr(obj, 'is_active'):
            obj.is_active=Status.N
        else:
            db.remove(obj)

        db.commit()

    def _current_username(self):
        if 'username' in session:
            return session['username']
        else:
            return 'Unknown'
