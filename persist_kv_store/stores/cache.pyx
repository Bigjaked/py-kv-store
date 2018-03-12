# cython: nonecheck = True
# cython: boundscheck = False

# -*- coding: utf-8 -*-
from collections import OrderedDict
from . import DEFAULT_CACHE_LIMIT

from cache cimport CacheMixin, LRUCache


cdef str none = 'None'

cdef class DefaultDict:
    def set(self, key, value):
        self[key] = value

cdef class CacheDummy:
    """
    Passthrough class for maintining functional api when a cache is not
    defined
    """
    cdef str delete(self, str key): return none

    def __set__(self, str key, object value): pass
    def __setitem__(self, str key, object value): pass
    cpdef void _set(self, str key, object value): pass
    cpdef void set(self, str key, object value): pass

    def __get__(self, str key, default): pass
    def __getitem__(self, str key): return none
    cpdef str _get(self, str key): return none
    cpdef str get(self, str key): return none

cdef class LRUCache:
    # cdef object _cache
    # cdef int _count
    # cdef int _limit
    def __cinit__(self, int _limit):
        self._cache = OrderedDict()
        self._count = 0
        self._limit = _limit
    def __init__(self, _limit):
        self._count = 0
        self._cache = OrderedDict()
        self._limit = _limit

    # cdef void set_(self, str key, object value):
    #     if key in self._cache:
    #         del self._cache[key]
    #     else:
    #         self._count += 1
    #         if self._count >= self._limit:
    #             self._cache.popitem()
    #             self._count -= 1
    #     self._cache[key] = value
    #
    # cdef object get_(self, str key):
    #     if key in self._cache:
    #         self._cache.move_to_end(key)
    #         return self._cache[key]
    #     else:
    #         return none
    # def __contains__(self, item):
    #     return item in self._cache

    def set(self, str key, object value):
        self.set_(key, value)
    def get(self, str key):
        return self.get_(key)

    def __getitem__(self, str key):
        return self.get_(key)
    def __setitem__(self, str key, object value):
        self.set_(key, value)

cdef class CacheMixin:
    def __cinit__(self, *args, **kwargs): pass

    def __init__(self, **kwargs):
        self.limit = getattr(kwargs, 'limit', DEFAULT_CACHE_LIMIT)
        self._cache = LRUCache(self.limit)
