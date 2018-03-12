# -*- coding: utf-8 -*-

from .basestore import SQLiteBase


class SqliteMemoryStore(SQLiteBase):
    def __init__(self, **kwargs):
        SQLiteBase.__init__(self, filename=':memory:', **kwargs)
        # CacheMixin.__init__(self, **kwargs)
    def set(self, key, value):
        self._set_cached(key, value)
        cdef str packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, str key):
        cdef object cached = self._get_cached(key)
        if cached is not 'None': return cached

        cdef str packed = self._query(key)
        if packed:
            return self._serializer.unserialize(packed)
        return None
    __getitem__ = get
    __setitem__ = set
