# cython: nonecheck = True
# cython: boundscheck = False

# -*- coding: utf-8 -*-

cdef class LRUCache:
    cdef:
        object _cache
        int _count
        int _limit
        void set_(self, str key, object value)
        object get_(self, str key)
        # void set(self, object key, object value)
        # object get(self, object key)

cdef class CacheMixin:
    cdef:
        int limit
        LRUCache _cache
        str _get_cached(self, str key)
        void _set_cached(self, str key, object value)
