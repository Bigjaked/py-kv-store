# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from .basestore import AbstractKvInterface
from .serializer import KeyValueSerializer
from .cache import CacheMixin

class RedisStore(AbstractKvInterface):
    _serializer = KeyValueSerializer()
    def __init__(self, redis_con):
        self._r = redis_con
    def set(self, key, value):
        self._set_cached(key, value)
        packed = self._serializer.serialize(value)
        self._r.set(key, packed)
        return 'set successfully'
    def get(self, key):
        cached = self._get_cached(key)
        if cached: return cached
        return self._serializer.deserialize(self._r.get(key))
    def __del__(self):
        try:
            self._r.close()
        except:
            pass

class RedisStoreWithCache(RedisStore, CacheMixin):
    def __init__(self, redis_con, **kwargs):
        RedisStore.__init__(self, redis_con=redis_con)
        CacheMixin.__init__(
            self,
            enabled=kwargs.get('cache', True),
            limit=kwargs.get('limit', 1000),
        )
