# -*- coding: utf-8 -*-
from persist_kv_store.stores import (
    SqlitePersistentStore,
    SqliteMemoryStore,
    RedisStore,
    MemcacheStore, )
from persist_kv_store.bench import bench, print_header, print_footer
from persist_kv_store import LRUCache, CacheDummy

if __name__ == '__main__':
    import redis
    import os

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    rd = RedisStore(redis.Redis(connection_pool=pool))

    benchmarks = [
        'overhead',
        # 'memcached',
        'sqlite-mem',
        # 'redis',
        'sqlite-disk',
    ]
    class Dummy:
        """
        Passthrough class for maintining functional api when a cache is not
        defined
        """
        def _set(self, key, value): pass
        def set(self, key, value): pass
        def _get(self, key): return 'None'
        def get(self, key): return 'None'
        __setitem__ = _set
        __getitem__ = _get
    run_cached = True
    its = 10000
    cache_size = 100
    bench_set = []
    ba = bench_set.append
    print_header(its)
    if 'overhead' in benchmarks:
        db = Dummy()
        ba(bench(db, its, "'pure overhead'"))

        db = CacheDummy()
        ba(bench(db, its, "'pure overhead'"))

        db = LRUCache(cache_size)
        ba(bench(db, its, "'subclassed OrderedDict'"))

    if 'memcached' in benchmarks:
        db = MemcacheStore()
        ba(bench(db, its))

    if 'sqlite-mem' in benchmarks:
        db = SqliteMemoryStore()
        ba(bench(db, its))

    if 'redis' in benchmarks:
        db = RedisStore(rd)
        ba(bench(db, its))

    if 'sqlite-disk' in benchmarks:
        db_file = 'test-db.db'
        if os.path.isfile(db_file): os.remove(db_file)
        db = SqlitePersistentStore(db_file)
        ba(bench(db, its))

        print('\nsorted table\n')

        print_header(its)

        for row in reversed(sorted(bench_set, key=lambda x: x[0])):
            print(row[1])
        print_footer()
