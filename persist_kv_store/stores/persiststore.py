# -*- coding: utf-8 -*-
from tinydb import Query, TinyDB
from tinydb.storages import JSONStorage, MemoryStorage

from .basecache import CacheBase, CacheHookedMixin, SimpleCache
from .basestore import SQLiteBase

class SqlitePersistentStore(SQLiteBase, CacheHookedMixin):
    def __init__(self, filename=':memory:'):
        self._cache = CacheBase(SimpleCache())
        self._cache_len = 0
        CacheHookedMixin.__init__(self)
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

class TinyDBPersistStore(CacheHookedMixin):
    def __init__(self, filename=None):
        CacheHookedMixin.__init__(self)
        self._cache = CacheBase(SimpleCache())
        self._cach_len = 0
        if filename is not None:
            self._db = TinyDB(filename, storage=JSONStorage)
        else:
            self._db = TinyDB(storage=MemoryStorage)
    def __del__(self):
        pass
    def set(self, key, value, **kwargs):
        self._db.insert(dict(key=key, value=value))
    def get(self, key, **kwargs):
        q = Query()
        return self._db.search(q.key == key)[0]
    def count(self):
        return self._db.count()
