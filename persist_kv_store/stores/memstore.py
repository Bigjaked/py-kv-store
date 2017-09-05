# -*- coding: utf-8 -*-
from .basestore import SQLiteBase, AbstractKvInterface
from .basecache import CacheBase, CacheHookedMixin, SimpleCache

class SqliteMemoryStore(SQLiteBase, AbstractKvInterface):
    def __init__(self, lock, **kwargs):
        SQLiteBase.__init__(
            self, filename=':memory:', lock=lock, limit=None)
    def set(self, key, value, **kwargs):
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key, **kwargs):
        if 'value' in kwargs: return kwargs['value']
        packed = self._query(key)
        if packed:
            return self._serializer.unserialize(packed)
        return None
    def __del__(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

class SqliteMemoryStoreWithCache(SqliteMemoryStore, CacheHookedMixin):
    def __init__(self, lock, **kwargs):
        CacheHookedMixin.__init__(self)
        SqliteMemoryStore.__init__(self, lock, **kwargs)
        self._cache = CacheBase(SimpleCache())
        self._cache_len = 0
