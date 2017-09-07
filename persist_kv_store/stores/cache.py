# -*- coding: utf-8 -*-
from collections import OrderedDict, defaultdict

from . import DEFAULT_CACHE_LIMIT

class DefaultDict(OrderedDict):
    def set(self, key, value):
        self[key] = value

class CacheDummy:
    """
    Passthrough class for maintining functional api when a cache is not
    defined
    """
    def delete(self, key): pass
    def __setitem__(self, key, value):
        return None
    def __getitem__(self, key): return None
    def get(self, key):
        return None
    def set(self, key, value):
        return None

# TODO: Create FIFOCache with OrderedDict
# TODO: performance of FIFOCache should be better than LRUCache

class LRUCache:
    """Store items in the order the keys were last added
    Overwriting or getting a key moves it to the top of the list
    part of the design of this cache is based on some of the optimizations
    listed below
        a = {i: i + 1 for i in range(1, 50)}
        def ty():
            try:
                c = a[60]
                return 0
            except KeyError:
                return 1
        def tt():
            if 60 in a:
                return 0
            else:
                return 1
    of the above 2 functions, in python 3.3 and up, tt is about 3 times faster
    than ty
        %%timeit -n 100000 -r 5 a=OrderedDict(); a.update({i:i for i in range(1,100)})
        del a[1]; a[1]=1
        162 ns ± 8.88 ns per loop (mean ± std. dev. of 5 runs, 100000 loops each)

        %%timeit -n 100000 -r 5 a=OrderedDict(); a.update({i:i for i in range(1,100)})
        a.move_to_end(1); a[1]=1
        228 ns ± 10.8 ns per loop (mean ± std. dev. of 5 runs, 100000 loops each)

    """
    def delete(self, key):
        """delete a key/value pair from the cache"""
        del self._cache[key]
        self._count -= 1
    def __init__(self, limit, **kwargs):
        self._cache = OrderedDict()
        self._count = 0
        self._limit = limit
    def set(self, key, value):
        """
        If the key is already present we need to move it to the end of
        of the dict before we update it.
        this is part of the least recently used LRU cache functionality
        """
        if key in self._cache:
            del self._cache[key]
        else:
            self._count += 1
            if self._count >= self._limit:
                self._cache.popitem()
                self._count -= 1
        self._cache[key] = value
    def get(self, key):
        """
        If the key is already present we need to move it to the end of
        of the dict, this is part of the least recently used LRU cache
        functionality

        # # look up key 3 times if found or 1 time if not
        # if key in self._cache:
        #     self._cache.move_to_end(key)
        # else:
        #     return None
        # return self._cache[key]
        # look up key 2 times if found or 1 time if not"""
        try:
            v = self._cache[key]
            self._cache.move_to_end(key)
            return v
        except KeyError:
            return None
    __delitem__ = delete
    __setitem__ = set
    __getitem__ = get

class CacheMixin:
    def __init__(self, **kwargs):
        cache = kwargs.get('cache', None)
        if cache is not None:
            # enable any dict like object as a cache
            if hasattr(cache, '__setitem__') and \
                hasattr(cache, '__getitem__'):
                self._cache = cache
            else:
                self._cache = LRUCache(
                    limit=kwargs.get('limit', DEFAULT_CACHE_LIMIT))
        else:
            # dummy cache to satisfy api
            self._cache = CacheDummy()
