# -*- coding: utf-8 -*-
from collections import OrderedDict

class SimpleCache(OrderedDict):
    """Store items in the order the keys were last added
    Also moves any requested key back to the beginning of the dict
    """
    def __setitem__(self, key, value, **kwargs):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value, **kwargs)

    def __getitem__(self, key):
        if key in self:
            self.move_to_end(key)
            return OrderedDict.__getitem__(self, k=key)
        else:
            return None
    def remove_last(self):
        a = self.popitem()

class CacheHookedMixin():
    def before_set(self, key, value, **kwargs):
        self._cache.set(key, value)
        return (key, value), kwargs
    def before_get(self, key, **kwargs):
        from_cache = self._cache.get(key)
        if from_cache: kwargs['value'] = from_cache
        return (key,), kwargs

class CacheBase:
    def __init__(self, cache, limit=100):
        self._cache = cache
        self._count = 0
        self._limit = limit
    def delete(self, key):
        del self._cache[key]
        self._count -= 1
    def set(self, key, value):
        self._cache[key] = value
        self._count = len(self._cache)
        if self._count > self._limit:
            self._cache.remove_last()
    def get(self, key, default=None):
        return self._cache[key]
    def __setitem__(self, key, value):
        self.set(key, value)
    def __getitem__(self, item):
        return self.get(item)
