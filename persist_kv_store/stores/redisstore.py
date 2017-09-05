# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from .basestore import AbstractKvInterface
from .serializer import KeyValueSerializer

class RedisStore(AbstractKvInterface):
    _serializer = KeyValueSerializer()
    def __init__(self, redis_con):
        self._r = redis_con
    def set(self, key, value, **kwargs):
        # packed = self._serializer.serialize(value)
        self._r.set(key, value)
        return 'set successfully'
    def get(self, key, **kwargs):
        v = self._r.get(key)
        # if v:
        #     return self._serializer.deserialize(v)
        # else:
        #     return None
        return v
    def __del__(self):
        try:
            self._r.close()
        except:
            pass
