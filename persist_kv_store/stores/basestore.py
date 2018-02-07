# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import OperationalError
from typing import Union
from .serializer import KeyValueSerializer

class KVBase(object):
    # Must be overwritten  in subclass
    def set(self, key, value): raise NotImplementedError
    def get(self, key): raise NotImplementedError
    def __del__(self): raise NotImplementedError

    def __getitem__(self, item, **kwargs): raise NotImplementedError
    def __setitem__(self, item, value, **kwargs): raise NotImplementedError

# noinspection SqlResolve
class SQLiteBase(KVBase):
    _serializer = KeyValueSerializer()
    _sql_table_exists = (
        'SELECT * FROM sqlite_master WHERE type=\'table\' AND name=?;')
    _sql_insert_many = (
        'REPLACE INTO kv_store (k, v) VALUES (?, ?);')
    _key_value_schema = (
        'CREATE TABLE kv_store (k TEXT PRIMARY KEY, v TEXT NOT NULL);')
    _sql_begin = 'BEGIN;'
    _sql_end = 'COMMIT;'

    def __init__(self, filename=':memory:', **kwargs):
        KVBase.__init__(self)
        self._since_last_commit = 0
        self._batch_size = kwargs.get('batch_size', 1)
        self._lock = kwargs.get('lock', None)
        self.current_batch = []
        self._current_batch_len = 0
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()
        if not self._table_exists('kv_store'):
            res = self.cur.execute(self._key_value_schema)
    def _acquire_lock(self):
        if self._lock is not None:
            self._lock.acquire()
    def _release_lock(self):
        if self._lock is not None:
            self._lock.release()
    @staticmethod
    def _get_result(executed_query):
        try:
            return executed_query[0]
        except IndexError:
            return executed_query
    def _table_exists(self, table_name: str) -> bool:
        """check to see if the table schema is in the database"""
        return bool(self.cur.execute(
            self._sql_table_exists, (table_name,)).fetchall())
    def flush(self, force=False):
        if force and self.current_batch or \
                self._current_batch_len >= self._batch_size:
            self._insert_many(self.current_batch)
            self.commit()
            self.current_batch = []
            self._current_batch_len = 0
    def _insert(self, key_: str, value):
        self._acquire_lock()
        self.current_batch.append((key_, value))
        self._current_batch_len += 1
        self.flush()
        self._release_lock()
    def _insert_many(self, batch: [str, ...]):
        self._acquire_lock()
        self.cur.execute(self._sql_begin)
        self.cur.executemany(self._sql_insert_many, batch)
        self.cur.execute(self._sql_end)
        self.commit()
        self._release_lock()
    def _query(self, key_: str) -> Union[bytes, bool]:
        self.flush(True)
        res = self.cur.execute(
            "SELECT v FROM kv_store WHERE k = ?;", (key_,)).fetchone()
        return res[0]
    def _count(self) -> int:
        q = "SELECT count(1) FROM kv_store;"
        res = self.cur.execute(q).fetchone()
        return self._get_result(res)
    def commit(self):
        self.con.commit()
        self._current_batch_len = 0

    def __del__(self):
        try:
            self.con.commit()
            self.cur.close()
        finally:
            self.con.close()
