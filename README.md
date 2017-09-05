#persist-kv-store

###Simple interface to a few key value stores






```text

PersistentStore:   Loops: 100
    ---get and set floating point values----
    set:  ops/s:   80.892,    s/op:    0.012
    get: Kops/s:  180.032,   ms/op:    0.006
    ------get and set 100 element dict------
    set:  ops/s:   76.240,    s/op:    0.013
    get: Kops/s:   41.708,   ms/op:    0.024
        Total Time:  0.00

MemcacheStore:   Loops: 100
    ---get and set floating point values----
    set: Kops/s:   32.373,   ms/op:    0.031
    get: Kops/s:   17.308,   ms/op:    0.058
    ------get and set 100 element dict------
    set: Kops/s:   14.559,   ms/op:    0.069
    get: Kops/s:   10.610,   ms/op:    0.094
        Total Time:  0.01

MemoryStore:   Loops: 100
    ---get and set floating point values----
    set: Kops/s:   60.182,   ms/op:    0.017
    get: Kops/s:  119.399,   ms/op:    0.008
    ------get and set 100 element dict------
    set: Kops/s:   13.778,   ms/op:    0.073
    get: Kops/s:   37.899,   ms/op:    0.026
        Total Time:  0.00

RedisStore:   Loops: 100
    ---get and set floating point values----
    set: Kops/s:    1.988,   ms/op:    0.503
    get: Kops/s:    3.369,   ms/op:    0.297
    ------get and set 100 element dict------
    set: Kops/s:    2.167,   ms/op:    0.461
    get: Kops/s:    2.929,   ms/op:    0.341
        Total Time:  0.03

TinyPersistStore:   Loops: 100
    ---get and set floating point values----
    set: Kops/s:   12.786,   ms/op:    0.078
    get: Kops/s:    3.647,   ms/op:    0.274
    ------get and set 100 element dict------
    set: Kops/s:    4.148,   ms/op:    0.241
    get: Kops/s:    2.257,   ms/op:    0.443
        Total Time:  0.04


```

Here is the same benchmark at a 1000 iterations
```text
PersistentStore: cache: True  Time: 12.73  Loops: 1000
    ---get and set floating point values----
    set:  ops/s:   78.542,    s/op:    0.013
    get: Mops/s:    1.109,   us/op:    0.902
    ------get and set 100 element dict------
    set:  ops/s:   73.003,    s/op:    0.014
    get: Mops/s:    1.055,   us/op:    0.948

MemoryStore: cache: True  Time:  0.04  Loops: 1000
    ---get and set floating point values----
    set: Kops/s:   23.705,   ms/op:    0.042
    get: Kops/s:  166.289,   ms/op:    0.006
    ------get and set 100 element dict------
    set: Kops/s:    9.535,   ms/op:    0.105
    get: Kops/s:   47.277,   ms/op:    0.021

RedisStore: cache: True  Time:  0.42  Loops: 1000
    ---get and set floating point values----
    set: Kops/s:    2.400,   ms/op:    0.417
    get: Kops/s:    3.222,   ms/op:    0.310
    ------get and set 100 element dict------
    set: Kops/s:    2.620,   ms/op:    0.382
    get: Kops/s:    2.806,   ms/op:    0.356

TinyPersistStore: cache: True  Time:  2.09  Loops: 1000
    ---get and set floating point values----
    set:  ops/s:  477.706,    s/op:    0.002
    get:  ops/s:  310.375,    s/op:    0.003
    ------get and set 100 element dict------
    set:  ops/s:   21.485,    s/op:    0.047
    get:  ops/s:   29.456,    s/op:    0.034

```