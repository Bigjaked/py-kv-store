# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query
from .basestore import SQLiteBase, AbstractKvInterface
class PersistentStore(SQLiteBase):
    def __init__(self, filename=':memory:'):
        self._cache = {}
        self._cache_len = 0
        SQLiteBase.__init__(self, filename=filename)
    def _cache_set(self, key, value):
        self._cache[key] = value
    def _cache_get(self, key):
        return self._cache.get(key, None)
    def _before_set(self, key, value):
        pass
    def _before_get(self, key):
        pass
    def set(self, key, value, cache=True):
        self._before_set(key, value)
        if cache: self._cache_set(key, value)
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key, cache=True):
        self._before_get(key, )
        if cache:
            cached_result = self._cache_get(key)
            if cached_result:
                return cached_result

        packed = self._query(key)
        if packed:
            return self._serializer.deserialize(packed)
        return None
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)

class TinyPersistStore(AbstractKvInterface):
    def __init__(self, filename):
        self._db = TinyDB(filename)
    def __del__(self):
        pass
    def set(self, key, value, cache=None):
        self._db.insert(dict(key=key, value=value))
    def get(self, key, cache=None):
        q = Query()
        return self._db.search(q.key==key)[0]
    def count(self):
        return self._db.count()
