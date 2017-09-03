# -*- coding: utf-8 -*-
import sqlite3

from .basestore import SQLiteBase

class PersistentStore(SQLiteBase):
    def __init__(self, filename=':memory:'):
        SQLiteBase.__init__(self, filename=filename)
        self._cache = {}
        self._cache_len = 0
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
        if not self._table_exists('kv_store'):
            res = self.cur.execute(self._key_value_schema)
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
    def get(self, key):
        self._before_get(key)
        cached_result = self._cache_get(key)
        if cached_result:
            return cached_result
        else:
            packed = self._query(key)
            if packed:
                return self._serializer.deserialize(packed)
        return None
    def __del__(self):
        self.cur.close()
        self.con.commit()
        self.con.close()
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)
