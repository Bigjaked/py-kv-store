# -*- coding: utf-8 -*-

import vedis
from . import DEFAULT_CACHE_LIMIT
from .serializer cimport KeyValueSerializer
cimport cache


cdef class CachedVedis(cache.CacheMixin):
    cdef KeyValueSerializer _serializer
    cdef str file_location
    cdef object _vedis_db
    def __init__(self, file_=':mem:', limit_=DEFAULT_CACHE_LIMIT):
        cache.CacheMixin.__init__(self, limit=limit_)
        self._serializer = KeyValueSerializer()
        self.file_location = file_
        self._vedis_db = vedis.Vedis(self.file_location)

    cdef set_(self, str key, object value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._vedis_db[key] = packed

    cdef get_(self, str key):
        if key in self._cache:
            return self._get_cached(key)
        cdef object packed = self._vedis_db[key]
        if packed:
            p = self._serializer.deserialize(self._vedis_db.get(key))
            self._set_cached(key, p)
            return p
        return None

    def set(self, object key, object value):
        self.set_(str(key), value)

    def get(self, key):
        return self.get_(str(key))

    @property
    def db(self):
        return self._vedis_db

    def __setitem__(self, object key, object value):
        self.set_(str(key), value)

    def __getitem__(self, object item):
        return self.get_(str(item))

    def __contains__(self, item):
        if str(item) in self._vedis_db:
            return True
        else:
            return False

    def __del__(self):
        try:
            self._vedis_db.close()
        except:
            pass
