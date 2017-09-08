# -*- coding: utf-8 -*-

from .cache import CacheMixin
from .basestore import SQLiteBase

class SqlitePersistentStore(SQLiteBase, CacheMixin):
    def __init__(self, filename, **kwargs):

        SQLiteBase.__init__(self, filename=filename)
        CacheMixin.__init__(self, **kwargs)
    def set(self, key, value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key):
        cached = self._get_cached(key)
        if cached is not 'None': return cached
        packed = self._query(key)
        if packed:
            return self._serializer.deserialize(packed)
        return None
    __getitem__ = get
    __setitem__ = set
