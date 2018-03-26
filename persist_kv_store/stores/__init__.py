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
from .cached_vedis import CachedVedis
# from .redisstore import RedisStore

