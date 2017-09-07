----------------
persist-kv-store
################

Simple interface to a few key value stores
------------------------------------------
Optional dependencies

ujson_

    ``pip install ujson``
msgpack-python_


    ``pip install msgpack-python``

----------
Benchmarks
##########

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


.. _msgpack-python::https://pypi.python.org/pypi/msgpack-python
.. _ujson:: https://pypi.python.org/pypi/ujson