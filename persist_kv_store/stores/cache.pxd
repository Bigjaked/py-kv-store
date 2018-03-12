# cython: nonecheck = True
# cython: boundscheck = False

# -*- coding: utf-8 -*-

cdef str none = 'None'



cdef class LRUCache:
    cdef object _cache
    cdef int _count
    cdef int _limit
    # def __cinit__(self, int _limit):
    #     self._cache = OrderedDict()
    #     self._count = 0
    #     self._limit = _limit
    # def __init__(self, _limit):
    #     self._count = 0
    #     self._cache = OrderedDict()
    #     self._limit = _limit

    cdef inline void set_(self, str key, object value):
        if key in self._cache:
            del self._cache[key]
        else:
            self._count += 1
            if self._count >= self._limit:
                self._cache.popitem()
                self._count -= 1
        self._cache[key] = value

    cdef inline object get_(self, str key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        else:
            return none
    # def __contains__(self, item):
    #     return item in self._cache

    # cdef inline void set(self, str key, object value):
    #     self.set_(key, value)
    # cdef inline object get(self, str key):
    #     return self.get_(key)

    # def __getitem__(self, str key):
    #     return self.get_(key)
    # def __setitem__(self, str key, object value):
    #     self.set_(key, value)

cdef class CacheMixin:
    cdef int limit
    cdef LRUCache _cache
    # def __cinit__(self, *args, **kwargs): pass
    #
    # def __init__(self, **kwargs):
    #     self.limit = getattr(kwargs, 'limit', DEFAULT_CACHE_LIMIT)
    #     self._cache = LRUCache(self.limit)
    cdef inline str _get_cached(self, str key):
        """standard cache get api"""
        return self._cache.get_(key)
    cdef inline void _set_cached(self, str key, str value):
        """standard cache set api"""
        self._cache.set_(key, value)
