# -*- coding: utf-8 -*-
from .cache import CacheMixin
from .basestore import SQLiteBase

class SqliteMemoryStore(SQLiteBase):
    def __init__(self, **kwargs):
        SQLiteBase.__init__(
            self, filename=':memory:', **kwargs)
    def set(self, key, value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key):
        cached = self._get_cached(key)
        if cached: return cached
        packed = self._query(key)
        if packed:
            return self._serializer.unserialize(packed)
        return None
    def __del__(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

class SqliteMemoryStoreWithCache(SqliteMemoryStore, CacheMixin):
    def __init__(self, lock, **kwargs):
        SqliteMemoryStore.__init__(self, **kwargs)
        CacheMixin.__init__(
            self,
            enabled=kwargs.get('cache', True),
            limit=kwargs.get('limit', 1000),
        )
