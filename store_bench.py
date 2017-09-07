# -*- coding: utf-8 -*-
from persist_kv_store.stores import (
    SqlitePersistentStore,
    SqliteMemoryStore,
    RedisStore,
    MemcacheStore, )
from persist_kv_store.bench import bench, print_header, print_footer
from persist_kv_store import LRUCache, DefaultDict, CacheDummy

if __name__ == '__main__':
    import redis
    import os

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    rd = RedisStore(redis.Redis(connection_pool=pool))

    benchmarks = [
        # 'overhead',
        # 'memcached',
        # 'sqlite-mem',
        # 'redis',
        'sqlite-disk',
    ]
    its = 1000
    cache_size = 1000

    print_header(its)
    if 'overhead' in benchmarks:
        db = CacheDummy()
        bench(db, its, "'pure overhead'")

        db = LRUCache(cache_size)
        bench(db, its, "'subclassed OrderedDict'")

    if 'memcached' in benchmarks:
        db = MemcacheStore()
        bench(db, its)

        db = MemcacheStore(cache=LRUCache(cache_size))
        bench(db, its, msg='LRUCache cache')

    if 'sqlite-mem' in benchmarks:
        db = SqliteMemoryStore()
        bench(db, its)

        db = SqliteMemoryStore(cache=LRUCache(cache_size))
        bench(db, its, msg='LRUCache cache')

    if 'redis' in benchmarks:
        db = RedisStore(rd)
        bench(db, its)

        db = RedisStore(rd, cache=LRUCache(cache_size))
        bench(db, its, msg='LRUCache cache')

    if 'sqlite-disk' in benchmarks:
        db_file = 'test-db.db'
        if os.path.isfile(db_file): os.remove(db_file)
        db = SqlitePersistentStore(db_file)
        bench(db, its)

        db_file = 'test-db1.db'
        if os.path.isfile(db_file): os.remove(db_file)
        db = SqlitePersistentStore(db_file, cache=LRUCache(cache_size))
        bench(db, its, msg='LRUCache cache')

    print_footer()
