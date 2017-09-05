# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from .basestore import AbstractKvInterface
from .serializer import KeyValueSerializer
from .basecache import CacheBase, CacheHookedMixin, SimpleCache

class RedisStore(AbstractKvInterface):
    _serializer = KeyValueSerializer()
    def __init__(self, redis_con):
        # AbstractKvInterface.__init__(self)
        self._r = redis_con
    def set(self, key, value, **kwargs):
        # packed = self._serializer.serialize(value)
        self._r.set(key, value)
        return 'set successfully'
    def get(self, key, **kwargs):
        if 'value' in kwargs: return kwargs['value']
        return self._r.get(key)
        # if v:
        #     return self._serializer.deserialize(v)
        # else:
        #     return None
        # return v
    def __del__(self):
        try:
            self._r.close()
        except:
            pass

class RedisStoreWithCache(RedisStore, CacheHookedMixin):
    def __init__(self, redis_con):
        self._cache = CacheBase(SimpleCache())
        self._cache_len = 0
        CacheHookedMixin.__init__(self)
        RedisStore.__init__(self, redis_con=redis_con)
