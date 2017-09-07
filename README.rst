persist-kv-store
================

Simple interface to a few key value stores
------------------------------------------
Optional dependencies

ujson_
.. _ujson: https://pypi.python.org/pypi/ujson

    ``pip install ujson``
msgpack-python_
.. _msgpack-python: https://pypi.python.org/pypi/msgpack-python

    ``pip install msgpack-python``


Benchmarks
==========

This is a baseline for the benchmarks, it represents the overhead of both the cache layer
and the structure of the code.

    +-----------------------------------------+---------------+---------------+---------------+---------------+
    |            1000000 Iterations           | set and get integers per/s    |     50 element dict per/s     |
    +=========================================+===============+===============+===============+===============+
    | CLASSNAME                               |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
    +=========================================+===============+===============+===============+===============+
    | CacheDummy 'pure overhead'              |    2.9 Mops/s |    3.1 Mops/s |    3.0 Mops/s |    3.2 Mops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | LRUCache 'subclassed OrderedDict'       |  698.7 Kops/s |    1.1 Mops/s |  739.7 Kops/s |    1.1 Mops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+

Here are a few benchmarks for the different memory based storage back ends.

    +-----------------------------------------+---------------+---------------+---------------+---------------+
    |             10000 Iterations            | set and get integers per/s    |     50 element dict per/s     |
    +=========================================+===============+===============+===============+===============+
    |   CLASSNAME                             |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
    +=========================================+===============+===============+===============+===============+
    | MemcacheStore                           |   47.5 Kops/s |   17.3 Kops/s |   40.4 Kops/s |   14.7 Kops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | MemcacheStore LRUCache cache            |   45.2 Kops/s |   31.4 Kops/s |   40.1 Kops/s |   30.5 Kops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | SqliteMemoryStore                       |   63.2 Kops/s |  158.7 Kops/s |   33.2 Kops/s |   90.0 Kops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | SqliteMemoryStore LRUCache cache        |   62.2 Kops/s |  245.4 Kops/s |   30.8 Kops/s |  138.9 Kops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | RedisStore                              |    2.8 Kops/s |    2.6 Kops/s |    2.6 Kops/s |    2.8 Kops/s |
    +-----------------------------------------+---------------+---------------+---------------+---------------+
    | RedisStore LRUCache cache               |    2.6 Kops/s |    5.1 Kops/s |    2.3 Kops/s |    5.8 Kops/s |
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
