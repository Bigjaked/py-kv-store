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

    pip install https://github.com/Bigjaked/py-kv-store/raw/master/dist/persist_kv_store-0.91.tar.gz


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

    >>>db['whatever-ascii-key-you-want'] = dict(can_i_use_dicts=True)
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

Benchmark was run on a MSI GS60 PRO-4k 32GB DDR4, i7-6700HQ
Main storage is a Samsung 950 PRO 512GB (2500 MB/s Read 1500 MB/s write)



+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME       100000 Iterations       |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |     2.40 M    |     4.60 M    |  417.14 ns    |  217.36 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=1000 keys          |     1.29 M    |     3.08 M    |  773.63 ns    |  324.68 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=10000 keys         |     1.20 M    |     3.00 M    |  832.32 ns    |  333.22 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache evict_after=100 keys           |     1.17 M    |     2.75 M    |  852.93 ns    |  364.18 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRU                                     |     1.37 M    |     2.14 M    |  727.29 ns    |  467.91 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SQLiteBase evict_after=1000.0 keys      |    39.06 K    |     3.28 M    |   25.60 us    |  304.63 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis Memory                            |   863.30 K    |     1.29 M    |    1.16 us    |  773.26 ns    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| Vedis Disk                              |   216.52 K    |   467.21 K    |    4.62 us    |    2.14 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+
