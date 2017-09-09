python key value kit
====================

Simple interface to a few key value stores
------------------------------------------
This is mainly just me playing around with git, reST, python packages, databases and cython.
None of this code runs anything in production, in fact, if anything, its just a bunch of
diferent database adapters thrown together in a package with a simple but fast LRU Cache based on
collections.OrderedDict
glued in with some crappy cython...


Installation
============
python 3.5+ but 3.2+ and 2.7 shouldn't require many changes

**build dependencies**

- cython install with

.. code-block:: shell

    pip install cython

**Optional dependencies**

- ujson_  can be installed with

.. _ujson: https://pypi.python.org/pypi/ujson

.. code-block:: shell

    pip install ujson

To install, download or clone (unzip if downloaded)
cd into the package folder and run

.. code-block:: shell

    python setup.py build_ext --inplace


Supported Key Stores
--------------------

- vedis_ via an `unofficial python adapter`_

    .. _vedis: https://vedis.symisc.net/

    .. _unofficial python adapter: https://github.com/coleifer/vedis-python

- memcached_ via pymemcache_

    .. _pymemcache: https://github.com/pinterest/pymemcache

    .. _memcached: https://memcached.org/

- redis_ via the `official adapter`_

    .. _redis: https://redis.io/

    .. _official adapter: https://github.com/andymccurdy/redis-py

- sqlite3 (memory and disk)


- Python OrderedDict subclass (faster than you would think)


Benchmarks
==========

Here is an example of how each benchmark is run

.. code-block:: python

    from timeit import default_timer()

    # time writes
    set_start = default_timer()
    for i in range(0, its):
        db['key-{i}'.format(i=i)] = i
    set_time = default_timer() - set_start

    # time reads
    get_start = default_timer()
    for i in range(0, its):
        db['key-{i}'.format(i=i)] = i
    get_time = default_timer() - get_start

Benchmark was run on a MSI GS60 PRO-4k 32GB RAM, i7-6700HQ @ 2.6Ghz TB to 3.1Ghz
Main storage is a Samsung 950 PRO 512GB (over 2000 Mbps read/write)


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
