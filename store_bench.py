# -*- coding: utf-8 -*-
from persist_kv_store.stores import (
    SQLiteBase as SqlitePersistentStore,
    SQLiteBase as SqliteMemoryStore,
    # RedisStore,
    MemcacheStore, )
from persist_kv_store.bench import bench, print_header, print_footer
from persist_kv_store import LRUCache, CacheDummy
from lru import LRU


def rm_file(file_):
    if os.path.isfile(file_):
        os.remove(file_)

if __name__ == '__main__':
    import os


    benchmarks = [
        'overhead',
        # 'memcached',
        'sqlite-mem',
        # 'redis',
        'vedis',
        # 'sqlite-disk',
    ]
    run_cached = True
    its = 100000
    cache_size = its / 100
    bench_set = []
    ba = bench_set.append
    if 'vedis' in benchmarks:
        try:
            from vedis import Vedis


            db = Vedis(':mem:')
            ba(bench(db, its, 'Memory'), )

            rm_file('vedis-test.db')
            db = Vedis('vedis-test.db')
            ba(bench(db, its, 'Disk'))
        except ImportError:
            print('vedis is not installed, skipping benchmark')
    if 'overhead' in benchmarks:
        db = CacheDummy()
        ba(bench(db, its, "'pure overhead'"))
        ca_size = int(its / 10)
        db = LRUCache(ca_size)
        ba(bench(db, its, 'evict_after={} keys'.format(ca_size)))
        ca_size = int(its / 100)
        db = LRUCache(ca_size)
        ba(bench(db, its, 'evict_after={} keys'.format(ca_size)))
        ca_size = int(its / 1000)
        db = LRUCache(ca_size)
        ba(bench(db, its, 'evict_after={} keys'.format(ca_size)))
        db = LRU(int(its))
        ba(bench(db, its))

    if 'memcached' in benchmarks:
        db = MemcacheStore()
        ba(bench(db, its))

    if 'sqlite-mem' in benchmarks:
        db = SqliteMemoryStore(':memory:', limit=cache_size, batch_size=2000)
        ba(bench(db, its, 'evict_after={} keys'.format(cache_size)))

    if 'redis' in benchmarks:
        try:
            import redis


            pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
            rd = RedisStore(redis.Redis(connection_pool=pool))
            db = RedisStore(rd)
            ba(bench(db, its))
        except ImportError:
            print('redis is not installed, skipping benchmark')

    if 'sqlite-disk' in benchmarks:
        db_file = 'test-db.db'
        rm_file(db_file)
        db = SqlitePersistentStore(db_file, batch_size=100)
        ba(bench(db, its))

    print_header(its)
    for row in reversed(sorted(bench_set, key=lambda x: x[0])):
        print(row[1])
        print_footer()
