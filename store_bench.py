# -*- coding: utf-8 -*-
from persist_kv_store.stores import (
    SqlitePersistentStore,
    SqliteMemoryStore,
    RedisStore,
    MemcacheStore, )
from persist_kv_store.bench import bench, print_header, print_footer
from persist_kv_store import LRUCache, CacheDummy

def rm_file(file_):
    if os.path.isfile(file_):
        os.remove(file_)

if __name__ == '__main__':
    import redis
    import os

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    rd = RedisStore(redis.Redis(connection_pool=pool))

    benchmarks = [
        'overhead',
        # 'memcached',
        # 'sqlite-mem',
        # 'redis',
        'vedis',
        # 'sqlite-disk',
    ]
    run_cached = True
    its = 100000
    cache_size = int(its / 10)
    bench_set = []
    ba = bench_set.append
    print_header(its)
    if 'vedis' in benchmarks:
        from vedis import Vedis
        db = Vedis(':mem:')
        ba(bench(db, its, method='[]'))

        rm_file('vedis-test.db')
        db = Vedis('vedis-test.db')
        ba(bench(db, its, method='[]'))
    if 'overhead' in benchmarks:
        db = CacheDummy()
        ba(bench(db, its, "'pure overhead'", method='[]'))
        print_footer()
        db = LRUCache(cache_size)
        ba(bench(db, its, "'subclassed OrderedDict'"))
        db = LRUCache(cache_size)
        ba(bench(db, its, "'subclassed OrderedDict'"))
        db = LRUCache(cache_size)
        print_footer()
        ba(bench(db, its, "'subclassed OrderedDict'", method='[]'))
        db = LRUCache(cache_size)
        ba(bench(db, its, "'subclassed OrderedDict'", method='[]'))

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
        rm_file(db_file)
        db = SqlitePersistentStore(db_file)
        ba(bench(db, its))
    print_footer()
    # print('\nsorted table\n')
    #
    # print_header(its)
    #
    # for row in reversed(sorted(bench_set, key=lambda x: x[0])):
    #     print(row[1])
    # print_footer()
