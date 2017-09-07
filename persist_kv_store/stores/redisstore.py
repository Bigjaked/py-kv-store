# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from .basestore import KVBase
from .cache import CacheMixin
from .serializer import KeyValueSerializer

class RedisStore(KVBase, CacheMixin):
    _serializer = KeyValueSerializer()
    def __init__(self, redis_con, **kwargs):
        CacheMixin.__init__(self, **kwargs)
        self._r = redis_con
    def set(self, key, value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._r.set(key, packed)
    def get(self, key):
        cached = self._get_cached(key)
        if cached is not None: return cached
        return self._serializer.deserialize(self._r.get(key))
    def __del__(self):
        try:
            self._r.close()
        except:
            pass
    __getitem__ = get
    __setitem__ = set
