# -*- coding: utf-8 -*-
from .basestore import SQLiteBase

class MemoryStore(SQLiteBase):
    def __init__(self, lock, **kwargs):
        SQLiteBase.__init__(
            self, filename=':memory:', lock=lock, limit=None)
    def set(self, key, value):
        packed = self._serializer.serialize(value)
        self._insert(key, packed)
    def get(self, key):
        packed = self._query(key)
        if packed:
            return self._serializer.unserialize(packed)
        return None
    def __del__(self):
        self.cur.close()
        self.con.commit()
        self.con.close()
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)
