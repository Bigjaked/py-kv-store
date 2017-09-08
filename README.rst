
persist-kv-store
===============

Simple interface to a few key value stores
------------------------------------------

**Optional dependencies**

- ujson_  can be installed with ``pip install msgpack-python``
- msgpack-python_ can be installed with ``pip install ujson``


.. _msgpack-python: https://pypi.python.org/pypi/msgpack-python

.. _ujson: https://pypi.python.org/pypi/ujson

Benchmarks
==========

This is a baseline for the benchmarks, it represents the overhead of both the cache layer
and the structure of the code.

+-----------------------------------------+---------------+---------------+---------------+---------------+
|            1000000 Iterations           | set and get integers per/s    |     50 element dict per/s     |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME                               |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |    2.9 Mops/s |    3.1 Mops/s |    3.0 Mops/s |    3.2 Mops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| LRUCache 'subclassed OrderedDict'       |  698.7 Kops/s |    1.1 Mops/s |  739.7 Kops/s |    1.1 Mops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+

Here are a few benchmarks for the different memory based storage back ends

+-----------------------------------------+---------------+---------------+---------------+---------------+
|             10000 Iterations            | set and get integers per/s    |     50 element dict per/s     |
+-----------------------------------------+---------------+---------------+---------------+---------------+
|   CLASSNAME                             |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
+=========================================+===============+===============+===============+===============+
| MemcacheStore                           |   47.8 Kops/s |   15.4 Kops/s |   45.9 Kops/s |   16.3 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| MemcacheStore LRUCache cache            |   44.7 Kops/s |  901.1 Kops/s |   42.1 Kops/s |  862.7 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SqliteMemoryStore                       |   74.0 Kops/s |  178.9 Kops/s |   50.6 Kops/s |   91.2 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SqliteMemoryStore LRUCache cache        |   69.4 Kops/s |  956.3 Kops/s |   46.7 Kops/s |    1.0 Mops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| RedisStore                              |    2.8 Kops/s |    3.0 Kops/s |    3.3 Kops/s |    3.2 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| RedisStore LRUCache cache               |    3.0 Kops/s |  690.7 Kops/s |    2.9 Kops/s |  628.4 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+

These benchmarks are for the back ends that write to disk

+-----------------------------------------+---------------+---------------+---------------+---------------+
|             1000 Iterations             | set and get integers per/s    |     50 element dict per/s     |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME                               |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
+=========================================+===============+===============+===============+===============+
| SqlitePersistentStore                   |   80.4  ops/s |  187.2 Kops/s |   75.0  ops/s |   84.9 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+
| SqlitePersistentStore LRUCache cache    |   78.7  ops/s |  972.1 Kops/s |   75.8  ops/s |  972.4 Kops/s |
+-----------------------------------------+---------------+---------------+---------------+---------------+


Tests on an odroid-c1+ (raspberry-pi-3 equivilent)
python 3.5.2
+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME        10000 Iterations       |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |   154.13 K    |   157.98 K    |    6.49 us    |    6.33 us    |
| LRUCache 'subclassed OrderedDict'       |    56.81 K    |    80.05 K    |   17.60 us    |   12.49 us    |
| SqliteMemoryStore                       |    15.34 K    |    13.00 K    |   65.20 us    |   76.91 us    |
| SqliteMemoryStore  w/lru cache          |    12.88 K    |    12.42 K    |   77.65 us    |   80.51 us    |
| SqlitePersistentStore  w/lru cache      |     3.78 K    |     7.05 K    |  264.64 us    |  141.77 us    |
| SqlitePersistentStore                   |     2.79 K    |     6.97 K    |  358.93 us    |  143.54 us    |
| MemcacheStore                           |     5.62 K    |     2.71 K    |  177.78 us    |  369.15 us    |
| MemcacheStore  w/lru cache              |     5.04 K    |     2.79 K    |  198.55 us    |  358.33 us    |
| RedisStore  w/lru cache                 |     1.77 K    |     2.12 K    |  565.97 us    |  471.79 us    |
| RedisStore                              |     1.85 K    |     1.99 K    |  540.46 us    |  501.96 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+

+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME        10000 Iterations       |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |   115.89 K    |   117.25 K    |    8.63 us    |    8.53 us    |
| LRUCache 'subclassed OrderedDict'       |    53.61 K    |    61.11 K    |   18.65 us    |   16.36 us    |
| SqliteMemoryStore  w/lru cache          |     7.70 K    |     9.13 K    |  129.81 us    |  109.55 us    |
| SqliteMemoryStore                       |     8.17 K    |     4.43 K    |  122.47 us    |  225.64 us    |
| SqlitePersistentStore  w/lru cache      |     3.30 K    |     5.80 K    |  302.89 us    |  172.54 us    |
| SqlitePersistentStore                   |     3.29 K    |     5.13 K    |  303.91 us    |  194.81 us    |
| MemcacheStore                           |     4.47 K    |     3.34 K    |  223.76 us    |  299.75 us    |
| MemcacheStore  w/lru cache              |     4.10 K    |     3.53 K    |  243.84 us    |  283.13 us    |
| RedisStore  w/lru cache                 |     2.47 K    |     3.04 K    |  404.77 us    |  328.59 us    |
| RedisStore                              |     1.83 K    |     2.57 K    |  546.90 us    |  388.57 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------+

+-----------------------------------------+---------------+---------------+---------------+---------------+
| CLASSNAME        10000 Iterations       |  sets per/s   |  gets per/s   |  sec per set  |  sec per get  |
+=========================================+===============+===============+===============+===============+
| CacheDummy 'pure overhead'              |   170.67 K    |   178.50 K    |    5.86 us    |    5.60 us    |
| Dummy 'pure overhead'                   |   150.00 K    |   152.77 K    |    6.67 us    |    6.55 us    |
| LRUCache 'subclassed OrderedDict'       |    75.85 K    |    79.78 K    |   13.18 us    |   12.53 us    |
| SqliteMemoryStore                       |    12.20 K    |    12.22 K    |   81.93 us    |   81.80 us    |
| SqlitePersistentStore                   |     3.46 K    |     7.83 K    |  288.63 us    |  127.67 us    |
+-----------------------------------------+---------------+---------------+---------------+---------------|