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

- cython
- ujson (optional)

Install with:

.. code-block:: shell

    pip install https://github.com/Bigjaked/py-kv-store/raw/master/dist/persist_kv_store-0.93.tar.gz


Supported Key Stores
--------------------

- Vedis (memory and disk)

- sqlite3 (memory and disk)

- Python OrderedDict subclass


Examples
========

.. code-block:: python
    >>>from persist_kv_store.stores import SqliteMemoryStore

    >>>db = SqliteMemoryStore()

    >>>db['whatever-utf-8-key-you-want'] = dict(can_i_use_dicts=True)
    >>>db['234234'] = 3
    >>>db['booleans'] = True



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

Benchmark was run on a MSI GS60 32GB DDR4, i7-6700HQ
Main storage is a Samsung 950 PRO 512GB 


+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME       1000000 Iterations      |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'call overhead'              |     4.13 M    |     8.68 M    |  241.85 ns    |  115.27 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=10000 keys         |     1.71 M    |     5.62 M    |  583.47 ns    |  177.92 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=1000 keys          |     1.86 M    |     5.41 M    |  538.40 ns    |  184.86 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=100000 keys        |     1.57 M    |     4.86 M    |  636.18 ns    |  205.69 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRU                                     |     1.88 M    |     3.59 M    |  531.02 ns    |  278.86 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis Memory                            |   542.27 K    |   674.98 K    |    1.84 us    |    1.48 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| CachedVedis Memory + LRUCache           |   446.52 K    |   610.61 K    |    2.24 us    |    1.64 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis Disk                              |   168.28 K    |   392.17 K    |    5.94 us    |    2.55 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| CachedVedis Disk + LRUCache             |   155.47 K    |   372.70 K    |    6.43 us    |    2.68 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
