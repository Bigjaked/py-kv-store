# -*- coding: utf-8 -*-
from tinydb import Query, TinyDB
from tinydb.storages import JSONStorage, MemoryStorage
from .cache import CacheMixin
from .basestore import AbstractKvInterface, SQLiteBase

class SqlitePersistentStore(SQLiteBase, CacheMixin):
    def __init__(self, filename, limit=1000):
        SQLiteBase.__init__(self, filename=filename)
        CacheMixin.__init__(self, limit=limit)
    def set(self, key, value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key):
        cached = self._get_cached(key)
        if cached: return cached
        packed = self._query(key)
        if packed:
            return self._serializer.deserialize(packed)
        return None
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)

class TinyDBPersistStore(AbstractKvInterface, CacheMixin):
    def __init__(self, filename=None, **kwargs):
        CacheMixin.__init__(
            self,
            enabled=kwargs.get('cache', True),
            limit=kwargs.get('limit', 1000),
        )
        if filename is not None:
            self._db = TinyDB(filename, storage=JSONStorage)
        else:
            self._db = TinyDB(storage=MemoryStorage)
    def __del__(self):
        pass
    def set(self, key, value):
        self._set_cached(key, value)
        self._db.insert(dict(key=key, value=value))
    def get(self, key):
        cached = self._get_cached(key)
        if cached: return cached
        q = Query()
        return self._db.search(q.key == key)[0]
    def count(self):
        return self._db.count()
