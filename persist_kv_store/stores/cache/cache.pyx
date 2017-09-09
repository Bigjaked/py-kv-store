# cython: nonecheck = True
# cython: boundscheck = False

# -*- coding: utf-8 -*-
from collections import OrderedDict

from . import DEFAULT_CACHE_LIMIT

cdef str none = 'None'

class DefaultDict:
    def set(self, str key, object value):
        self[key] = value

cdef class CacheDummy:
    """
    Passthrough class for maintining functional api when a cache is not
    defined
    """
    cdef str delete(self, str key): return none

    def __set__(self, str key not None, object value not None): pass
    def __setitem__(self, str key, object value): pass
    cpdef void _set(self, str key, object value): pass
    cpdef void set(self, str key, object value): pass

    def __get__(self, str key not None, default not None): pass
    def __getitem__(self, str key): return none
    cpdef str _get(self, str key): return none
    cpdef str get(self, str key): return none

cdef class LRUCache:
    cdef object _cache
    cdef int _count
    cdef int _limit
    def __cinit__(self, int _limit):
        self._cache = OrderedDict()
        self._count = 0
        self._limit = _limit
    def __init__(self, _limit):
        self._count = 0
        self._cache = OrderedDict()
        self._limit = _limit
    cdef _set(self, str key, object value):
        if key in self._cache:
            self._cache.__delitem__(key)
        else:
            self._count += 1
            if self._count >= self._limit:
                self._cache.popitem()
                self._count -= 1
        # self._cache[key] = value
        self._cache.__setitem__(key, value)
    cdef object _get(self, str key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache.__getitem__(key)
        else:
            return none

    cpdef set(self, str key, object value):
        self._set(key, value)
    cpdef object get(self, str key):
        return self._get(key)

    def __getitem__(self, str key):
        return self._get(key)
    def __setitem__(self, str key, object value):
        self._set(key, value)

cdef class CacheMixin:
    cdef int limit
    cdef LRUCache _cache
    def __init__(self, **kwargs):
        limit = kwargs.get('limit', DEFAULT_CACHE_LIMIT)
        self._cache = LRUCache(limit)
    # api convienience  methods
    cpdef object _get_cached(self, str key):
        """standard cache get api"""
        return self._cache._get(key)
    cpdef _set_cached(self, str key, object value):
        """standard cache set api"""
        self._cache._set(key, value)
