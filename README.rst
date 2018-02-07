

Simple interface to a few key value stores
------------------------------------------
This is mainly just me playing around with git, reST, python packages, and cython; but it is also
a fully functioning key value store with both memory and disk implementations using sqlite and some
other key value stores.

All storage back ends have dict-like interfaces as well as a default LRU cache based off of
OrderedDict.


Installation
============
python 3.5+

**build dependencies**

- cython install with

.. code-block:: shell

    pip install cython

**Optional dependencies**

- ujson_  can be installed with

.. _ujson: https://pypi.python.org/pypi/ujson

.. code-block:: shell

    pip install ujson

To install

.. code-block:: shell

    pip install https://github.com/Bigjaked/py-kv-store/raw/master/dist/persist_kv_store-0.91.tar.gz


Supported Key Stores
--------------------

- memcached_ via pymemcache_

    .. _pymemcache: https://github.com/pinterest/pymemcache

    .. _memcached: https://memcached.org/

- redis_ via the `official adapter`_

    .. _redis: https://redis.io/

    .. _official adapter: https://github.com/andymccurdy/redis-py

- sqlite3 (memory and disk)


- Python OrderedDict subclass


Benchmarks
==========

Here is an example of how each benchmark is run

.. code-block:: python

    from timeit import default_timer

    # time writes
    set_start = default_timer()
    for i in range(0, its):
        db['key-{i}'.format(i=i)] = i
    set_time = default_timer() - set_start

    # time reads
    get_start = default_timer()
    for i in range(0, its):
        a = db['key-{i}'.format(i=i)]
    get_time = default_timer() - get_start

Benchmark was run on a MSI GS60 PRO-4k 32GB DDR4, i7-6700HQ
Main storage is a Samsung 950 PRO 512GB (2500 MB/s Read 1500 MB/s write)


No batching (except for sqlitePersistentStore)


+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME       1000000 Iterations      |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |     2.40 M    |     2.38 M    |  416.89 ns    |  420.90 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=1000               |     1.11 M    |     2.04 M    |  898.27 ns    |  491.15 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=10000              |     1.06 M    |     2.03 M    |  945.26 ns    |  493.69 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=100000             |   981.33 K    |     1.72 M    |    1.02 us    |  580.75 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis     in memory                     |   398.76 K    |   462.32 K    |    2.51 us    |    2.16 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis     on disk                       |   125.85 K    |   210.57 K    |    7.95 us    |    4.75 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SqliteMemoryStore                       |    80.04 K    |   139.16 K    |   12.49 us    |    7.19 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| MemcacheStore                           |    44.70 K    |    19.00 K    |   22.37 us    |   52.63 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SqlitePersistentStore                   |     6.57 K    |    26.51 K    |  152.32 us    |   37.73 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| RedisStore                              |     3.00 K    |     3.12 K    |  333.61 us    |  320.66 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
