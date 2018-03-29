# cython: nonecheck = True
# cython: boundscheck = False

# -*- coding: utf-8 -*-

cdef class LRUCache:
    cdef:
        object _cache
        int _count
        int _limit
        void set_(self, object key, object value)
        object get_(self, object key)
        # void set(self, object key, object value)
        # object get(self, object key)

cdef class CacheMixin:
    cdef:
        int limit
        LRUCache _cache
        object _get_cached(self, object key)
        void _set_cached(self, object key, object value)
