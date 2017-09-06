# -*- coding: utf-8 -*-

# import msgpack
import ujson

from pymemcache.client.base import Client

from .cache import CacheMixin
from .basestore import AbstractKvInterface

def pack(key, value):
    # return msgpack.packb(value, use_bin_type=True), 1
    return ujson.dumps(value), 1
def unpack(key, value, flags):
    if flags == 1:
        # return msgpack.unpackb(value, use_list=False), 1
        return ujson.loads(value)
    return value
    # raise Exception(f'Unkown de-serialization flag {flags}')

class MemcacheStore(AbstractKvInterface):
    def __init__(self, host='127.0.0.1', port=11211):
        self._memcache = Client(
            (host, port), serializer=pack, deserializer=unpack)
    def __del__(self):
        try:
            self._memcache.close()
        except: pass
    def set(self, key, value):
        self._set_cached(key, value)
        self._memcache.set(key, value)
    def get(self, key):
        cached = self._get_cached(key)
        if cached: return cached
        return self._memcache.get(key, None)

class MemcacheStoreWithCache(MemcacheStore, CacheMixin):
    def __init__(self, **kwargs):
        MemcacheStore.__init__(self)
        CacheMixin.__init__(
            self,
            enabled=kwargs.get('cache', True),
            limit=kwargs.get('limit', 1000),
        )
