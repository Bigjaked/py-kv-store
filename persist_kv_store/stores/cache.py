# -*- coding: utf-8 -*-
from collections import OrderedDict

class DefaultDictCache:
    """Store items in the order the keys were last added
    Overwriting or getting a key moves it to the top of the list
    """
    def __init__(self, limit, prune):
        self._cache = OrderedDict()
        self._count = 0
        self._limit = limit
        self._prune = prune
    def set(self, key, value):
        """alias for __setitem__"""
        self.__setitem__(key, value)
    def get(self, key):
        """alias for __getitem__"""
        return self.__getitem__(key)
    def delete(self, key):
        """delete a key/value pair from the cache"""
        del self._cache[key]
        self._count -= 1
    def remove_last(self):
        """remove the key/value pair that is least used"""
        a = self._cache.popitem()
    def prune_cache(self):
        """pop `self._prune` of the least used items in the cache"""
        a = [self.remove_last() for i in range(self._prune)]
        self._count -= self._prune
    def __setitem__(self, key, value):
        if key in self._cache:
            del self._cache[key]
        else:
            self._count += 1
            if self._count >= self._limit:
                self.prune_cache()
        self._cache.__setitem__(key, value)
    def __getitem__(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache.__getitem__(key)
        else:
            return None

class CacheMixin:
    def __init__(self, enabled=True, limit=500):
        prune = int(limit * 0.05)
        self._cache_enabled = enabled
        self._cache = DefaultDictCache(limit=limit, prune=prune)
    def _set_cache(self, key, value):
        if self._cache_enabled:
            self._cache.set(key, value)
    def _get_cache(self, key):
        if self._cache_enabled:
            from_cache = self._cache.get(key)
            return from_cache
        return None
