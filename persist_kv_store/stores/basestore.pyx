# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime

cimport serializer, cache

#cythn: boundscheck=False, wraparound=False, nonecheck=False

cdef:
    str SQL_TABLE_EXISTS = 'SELECT * FROM sqlite_master WHERE type=\'table\' AND name=?;'
    str SQL_INSERT_MANY = 'REPLACE INTO kv_store (k, v) VALUES (?, ?);'
    str SQL_KV_SCHEMA = 'CREATE TABLE kv_store (k TEXT PRIMARY KEY, v TEXT NOT NULL);'
    str SQL_QUERY = "SELECT v FROM kv_store WHERE k = ?;"
    str SQL_COUNT = "SELECT count(1) FROM kv_store;"
    str SQL_BEGIN = 'BEGIN;'
    str SQL_END = 'COMMIT;'
    str cNONE = 'None'
    dict custom_serializers = {
        '__datetime__': {
            'serialize': lambda dt: {'type-key': '__datetime__', 'val': dt.isoformat()},
            'deserialize': lambda o: datetime.strptime(o['val'], "%Y%m%dT%H:%M:%S.%f")
        }
    }
    dict types = {datetime: '__datetime__'}

cdef class SQLiteBase(cache.CacheMixin):
    cdef:
        serializer.KeyValueSerializer _serializer
        int _since_last_commit
        int _batch_size
        bint _ctx_manager_open
        object _lock
        list current_batch
        int _current_batch_len
        object con
        object cur
    def __cinit__(self, str filename, **kwargs):
        self._serializer = serializer.KeyValueSerializer()
        self._batch_size = getattr(kwargs, 'batch_size', 1)
        self._lock = getattr(kwargs, 'lock', 0)
        self._since_last_commit = 0
        self._current_batch_len = 0
        self._ctx_manager_open = False

    def __init__(self, str filename, **kwargs):
        cache.CacheMixin.__init__(self, **kwargs)
        self.current_batch = []
        filename = filename or ':memory:'
        self.con = sqlite3.connect(
          filename, check_same_thread=False, isolation_level=None)
        self.cur = self.con.cursor()
        if not self._table_exists('kv_store'):
            res = self.cur.execute(SQL_KV_SCHEMA)

    cdef void _acquire_lock(self):
        if self._lock:
            self._lock.acquire()

    cdef void _release_lock(self):
        if self._lock:
            self._lock.release()

    cdef object _get_result(self, executed_query):
        try:
            return executed_query[0]
        except IndexError:
            return executed_query

    cdef int _table_exists(self, str table_name):
        """check to see if the table schema is in the database"""
        if self.cur.execute(SQL_TABLE_EXISTS, (table_name,)).fetchall():
            return 1
        else:
            return 0
    def flush(self):
        self._flush()

    cdef _flush(self, bint force=False):
        if force and self.current_batch or \
          self._current_batch_len >= self._batch_size:
            if self._ctx_manager_open is 0:
                self._insert_many(self.current_batch)
                self.commit()
                self.current_batch = []
                self._current_batch_len = 0

    cdef _insert(self, str key_, value):
        self._acquire_lock()
        self.current_batch.append((key_, value))
        self._current_batch_len += 1
        self._flush()
        self._release_lock()

    cdef _insert_many(self, list batch):
        self._acquire_lock()
        self.cur.execute(SQL_BEGIN)
        self.cur.executemany(SQL_INSERT_MANY, batch)
        self.cur.execute(SQL_END)
        self.commit()
        self._release_lock()

    cdef object  _query(self, str key_):
        self._flush(True)
        cdef object res = self.cur.execute(
          SQL_QUERY, (key_,)).fetchone()
        try:
            if res[0] is not None:
                return res[0]
            return cNONE
        except (IndexError, TypeError):
            return cNONE

    cdef int _count(self):
        cdef int res = self.cur.execute(SQL_COUNT).fetchone()[0]
        return res

    cdef void commit(self):
        self.con.commit()
        self._current_batch_len = 0

    cpdef void set(self, object key, object value):
        cdef str k = str(key)
        self._set_cached(k, value)
        cdef str packed = self._serializer.serialize(value)
        self._insert(k, value)

    cpdef object get(self, object key):
        cdef str k = str(key)
        cdef object cached = self._get_cached(k)
        if cached is not cNONE: return cached
        cdef object packed = self._query(k)
        if packed and packed is not cNONE:
            return self._serializer.unserialize(packed)
        return cNONE
    def __contains__(self, object item):
        if self.get(item) is not cNONE:
            return True
        return False

    def __enter__(self):
        self._flush(True)
        self._ctx_manager_open = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not any(exc_type, exc_val, exc_tb):
            self._flush(True)
        self._ctx_manager_open = False
    def __getitem__(self, str item):
        return self.get(item)
    def __setitem__(self, str key, object value):
        self.set(key, value)

    def __del__(self):
        try:
            try:
                self.con.commit()
                self.cur.close()
            finally:
                self.con.close()
        except Exception as e:
            pass
