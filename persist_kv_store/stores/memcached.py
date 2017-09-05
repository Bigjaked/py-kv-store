# -*- coding: utf-8 -*-

# import msgpack
from pymemcache.client.base import Client
from .basestore import AbstractKvInterface
from .basecache import CacheBase, CacheHookedMixin, SimpleCache
import ujson

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
    def set(self, key, value, **kwargs):
        self._memcache.set(key, value)
    def get(self, key, **kwargs):
        if 'value' in kwargs: return kwargs['value']
        return self._memcache.get(key, None)

class MemcacheStoreWithCache(MemcacheStore, CacheHookedMixin):
    def __init__(self):
        CacheHookedMixin.__init__(self)
        MemcacheStore.__init__(self)
        self._cache = CacheBase(SimpleCache())
        self._cache_len = 0
