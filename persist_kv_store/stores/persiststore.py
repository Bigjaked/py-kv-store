# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage, MemoryStorage
from tinydb.middlewares import CachingMiddleware
from .basestore import SQLiteBase, AbstractKvInterface
from .basecache import CacheBase, CacheHookedMixin
class PersistentStore(SQLiteBase, CacheHookedMixin):
    def __init__(self, filename=':memory:'):
        self._cache = CacheBase()
        self._cache_len = 0
        SQLiteBase.__init__(self, filename=filename)
    def set(self, key, value, **kwargs):
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key, **kwargs):
        if 'value' in kwargs: return kwargs['value']
        packed = self._query(key)
        if packed:
            return self._serializer.deserialize(packed)
        return None
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)

class TinyPersistStore(AbstractKvInterface):
    def __init__(self, filename=None):
        if filename is not None:
            self._db = TinyDB(filename, storage=CachingMiddleware(JSONStorage))
        else:
            self._db = TinyDB(storage=CachingMiddleware(MemoryStorage))
    def __del__(self):
        pass
    def set(self, key, value, **kwargs):
        self._db.insert(dict(key=key, value=value))
    def get(self, key, **kwargs):
        q = Query()
        return self._db.search(q.key == key)[0]
    def count(self):
        return self._db.count()
