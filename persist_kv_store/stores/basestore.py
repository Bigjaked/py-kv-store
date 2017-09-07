# -*- coding: utf-8 -*-
import sqlite3
from typing import Union
from .serializer import KeyValueSerializer

class KVBase(object):
    # Must be overwritten  in subclass
    def set(self, key, value): raise NotImplementedError
    def get(self, key): raise NotImplementedError
    def __del__(self): raise NotImplementedError

    # api convienience  methods
    def _get_cached(self, key):
        """standard cache get api"""
        # Call getitem directly for max performance
        # if there is no cache, the dummy class will return None
        return self._cache.get(key)
    def _set_cached(self, key, value):
        """standard cache set api"""
        # Call getitem directly for max performance
        # if there is no cache, it will pass silently through the dummy class
        self._cache.set(key, value)

    def __getitem__(self, item, **kwargs): raise NotImplementedError
    def __setitem__(self, item, value, **kwargs): raise NotImplementedError

class SQLiteBase(KVBase):
    _serializer = KeyValueSerializer()
    _key_value_schema = ('CREATE TABLE kv_store ('
                         '  k TEXT PRIMARY KEY,'
                         '  v TEXT NOT NULL'
                         ');')

    def __init__(self, filename=':memory:', **kwargs):
        KVBase.__init__(self)
        self._since_last_commit = 0
        self._batch_size = kwargs.get('batch_size', 100)
        self.current_batch = []
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()
        if not self._table_exists('kv_store'):
            res = self.cur.execute(self._key_value_schema)
    @staticmethod
    def _get_result(executed_query):
        if isinstance(executed_query, (tuple, list)):
            if len(executed_query) == 1:
                return executed_query[0]
        else:
            return executed_query
    def _table_exists(self, table_name: str) -> bool:
        """check to see if the table schema is in the database"""
        query = (
            "SELECT * FROM sqlite_master "
            "WHERE type='table' AND name=:name;")
        res = self.cur.execute(query, (table_name,)).fetchall()
        return bool(res)
    def _insert(self, key_: str, value: bytes):
        # q = "INSERT OR REPLACE INTO kv_store (k, v)" \
        #     " VALUES (:key_, :value);"
        # self.cur.execute(q, (key_, value))

        # self._since_last_commit += 1
        # if self._since_last_commit > self._batch_size:

        self.current_batch.append((key_, value))
        if not len(self.current_batch) < self._batch_size:
            self._insert_many(self.current_batch)
            self.commit()
            self.current_batch = []
    def _insert_many(self, batch: [(str, str), ...]):
        values = tuple("('{}','{}')".format(k, v) for k, v in batch)
        q = "INSERT OR REPLACE INTO kv_store (k, v)" \
            " VALUES %s;" % ','.join(values)
        self.cur.execute(q)
        self.commit()
    def _query(self, key_: str) -> Union[bytes, bool]:
        q = "SELECT v FROM kv_store WHERE k = :key_;"
        res = self.cur.execute(q, (key_,)).fetchone()
        return self._get_result(res)
    def _count(self) -> int:
        q = "SELECT count(1) FROM kv_store;"
        res = self.cur.execute(q).fetchone()
        return self._get_result(res)
    def commit(self):
        self.con.commit()
        self._since_last_commit = 0

    def __del__(self):
        try:
            self.con.commit()
        except:
            pass
        try:
            self.cur.close()
        except:
            pass
        try:
            self.con.close()
        except:
            pass
