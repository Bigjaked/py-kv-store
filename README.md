# persist-kv-store

### Simple interface to a few key value stores



Here is a quick benchmark of the different backends. 
Note: the `SqlitePersistentStore` and the  `TinyDBPersistStore` both have caching enabled. 
The `TinyDBPersistStore` is using the in memory store because the disk store, would take 
more than 5 minutes for 1000 iterations.

```text
Basic testing overhead (defaultdict):   Loops: 1000
    ---get and set floating point values----
    set: Mops/s:    2.693,   us/op:    0.371
    get: Mops/s:    3.637,   us/op:    0.275
    ------get and set 100 element dict------
    set: Kops/s:   57.303,   ms/op:    0.017
    get: Mops/s:    1.982,   us/op:    0.504
        Total Time:   0.0005

SqlitePersistentStore:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:  266.728,   ms/op:    0.004
    get: Kops/s:  257.949,   ms/op:    0.004
    ------get and set 100 element dict------
    set: Kops/s:   44.771,   ms/op:    0.022
    get: Kops/s:  263.837,   ms/op:    0.004
        Total Time:   0.0038

MemcacheStore:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:   46.658,   ms/op:    0.021
    get: Kops/s:   18.710,   ms/op:    0.053
    ------get and set 100 element dict------
    set: Kops/s:   22.725,   ms/op:    0.044
    get: Kops/s:   14.035,   ms/op:    0.071
        Total Time:   0.0713

SqliteMemoryStore:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:   61.986,   ms/op:    0.016
    get: Kops/s:  183.105,   ms/op:    0.005
    ------get and set 100 element dict------
    set: Kops/s:   21.201,   ms/op:    0.047
    get: Kops/s:   47.124,   ms/op:    0.021
        Total Time:   0.0212

RedisStore:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:    2.824,   ms/op:    0.354
    get: Kops/s:    3.333,   ms/op:    0.300
    ------get and set 100 element dict------
    set: Kops/s:    2.978,   ms/op:    0.336
    get: Kops/s:    3.207,   ms/op:    0.312
        Total Time:   0.3118
```

```text
Basic testing overhead (defaultdict):   Loops: 1000
    ---get and set floating point values----
    set: Mops/s:    2.679,   us/op:    0.373
    get: Mops/s:    2.985,   us/op:    0.335
    ------get and set 100 element dict------
    set: Kops/s:   52.832,   ms/op:    0.019
    get: Mops/s:    2.722,   us/op:    0.367
        Total Time:   0.0004

SqlitePersistentStore:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:  188.970,   ms/op:    0.005
    get: Kops/s:  256.771,   ms/op:    0.004
    ------get and set 100 element dict------
    set: Kops/s:   48.487,   ms/op:    0.021
    get: Kops/s:  217.817,   ms/op:    0.005
        Total Time:   0.0046

MemcacheStoreWithCache:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:  206.835,   ms/op:    0.005
    get: Kops/s:  211.290,   ms/op:    0.005
    ------get and set 100 element dict------
    set: Kops/s:   48.056,   ms/op:    0.021
    get: Kops/s:  204.959,   ms/op:    0.005
        Total Time:   0.0049

SqliteMemoryStoreWithCache:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:  233.037,   ms/op:    0.004
    get: Kops/s:  255.578,   ms/op:    0.004
    ------get and set 100 element dict------
    set: Kops/s:   49.516,   ms/op:    0.020
    get: Kops/s:  249.041,   ms/op:    0.004
        Total Time:   0.0040

RedisStoreWithCache:   Loops: 1000
    ---get and set floating point values----
    set: Kops/s:  202.630,   ms/op:    0.005
    get: Kops/s:  217.275,   ms/op:    0.005
    ------get and set 100 element dict------
    set: Kops/s:   48.022,   ms/op:    0.021
    get: Kops/s:  212.728,   ms/op:    0.005
        Total Time:   0.0047

```