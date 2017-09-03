# -*- coding: utf-8 -*-
import sqlite3
from typing import Union
from .serializer import KeyValueSerializer

DEBUG = False
class AbstractKvInterface(object):
    def set(self, key, value): raise NotImplementedError
    def get(self, key): raise NotImplementedError
    def __del__(self): raise NotImplementedError
    def __getitem__(self, item):
        return self.get(item)
    def __setitem__(self, key, value):
        self.set(key, value)

class SQLiteBase(AbstractKvInterface):
    _serializer = KeyValueSerializer()
    _key_value_schema = (
        'CREATE TABLE kv_store ('
        '  k TEXT PRIMARY KEY,'
        '  v BLOB NOT NULL'
        ');'
    )

    def __init__(self, filename=':memory:', **kwargs):
        self.lock = kwargs['lock']
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
        with self.lock:
            res = self.cur.execute(query, (table_name,)).fetchall()
        return bool(res)
    def _insert(self, key_: str, value: bytes):
        q = "INSERT OR REPLACE INTO kv_store (k, v)" \
            " VALUES (:key_, :value);"
        if DEBUG:
            print(q.replace(':key_', key_).replace(
                ':value', str(value)))

        with self.lock:
            self.cur.execute(q, (key_, value))
            self.con.commit()

    def _query(self, key_: str) -> Union[bytes, bool]:
        q = "SELECT v FROM kv_store WHERE k = :key_;"
        if DEBUG: print(q.replace('key_', key_))
        with self.lock:
            res = self.cur.execute(q, (key_,)).fetchone()
        try:
            return res[0]
        except:
            return False
    def _count(self) -> int:
        q = "SELECT count(1) FROM kv_store;"
        with self.lock:
            res = self.cur.execute(q).fetchone()
        try:
            return self._get_result(res)
        except:
            return False
