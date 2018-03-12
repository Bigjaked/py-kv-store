# -*- coding: utf-8 -*-

from .config import *


try:
    import ujson
except ImportError:
    print("Warning failed to import 'ujson' falling back to 'json' ")
    print("For a performance increase 'pip install ujson' ")
    import json as ujson

from .basestore import SQLiteBase
from .cache import LRUCache, DefaultDict, CacheDummy, CacheMixin
from .serializer import KeyValueSerializer
# from .memstore import SqliteMemoryStore
# from .persiststore import SqlitePersistentStore
# from .redisstore import RedisStore

try:
    from .memcached import MemcacheStore
except ImportError:
    print('pymemcache is required for the memcache adapter')
