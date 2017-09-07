# persist-kv-store

## Simple interface to a few key value stores

### Optional dependencies


```text
 ---------------------------------------------------------------------------------------------------------
|             10000 Iterations            |    set and get ints per/s     | set and get 50 el dict per/s  |
 ---------------------------------------------------------------------------------------------------------
| CLASSNAME                               |   sets p/s    |   gets p/s    |   sets p/s    |   gets p/s    |
 ---------------------------------------------------------------------------------------------------------
| DefaultDict 'no evict functions'        |    2.4 Mops/s |    2.8 Mops/s |    2.4 Mops/s |    3.2 Mops/s |
| C_LRU 'lru_dict c module'               |    1.5 Mops/s |    1.5 Mops/s |    1.5 Mops/s |    1.7 Mops/s |
| LRUCache 'subclassed OrderedDict'       |    1.1 Mops/s |    1.4 Mops/s |  952.9 Kops/s |    1.6 Mops/s |
 ---------------------------------------------------------------------------------------------------------

```

Here is a quick benchmark of the different backends. 
Note: the `SqlitePersistentStore` and the  `TinyDBPersistStore` both have caching enabled. 
The `TinyDBPersistStore` is using the in memory store because the disk store, would take 
more than 5 minutes for 1000 iterations.

```text

```

```text

```