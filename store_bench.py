# -*- coding: utf-8 -*-
# from persist_kv_store.stores.persiststore import PersistentStore
# from persist_kv_store.stores.memstore import MemoryStore
# from persist_kv_store.stores.redisstore import RedisStore
from persist_kv_store.stores import (PersistentStore, TinyPersistStore, MemoryStore,
    RedisStore, )
def fmt(val):
    if val > 1:
        if val > 1e9:
            return 'G', val / 1e9
        elif val > 1e6:
            return 'M', val / 1e6
        elif val > 1e3:
            return 'K', val / 1e3
        else:
            return ' ', val
    else:
        if val < 1e-8:
            return 'ns', val * 1e9
        elif val < 1e-6:
            return 'us', val * 1e6
        elif val < 1e-3:
            return 'ms', val * 1e3
        else:
            return ' s', val

def l_json(x, ln=500):
    return {f'k-{n}': n * i for n in range(ln)}

if __name__ == '__main__':
    from random import randrange
    from timeit import default_timer as clockit
    from math import pi
    import redis
    import os

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    rd = RedisStore(redis.Redis(connection_pool=pool))

    db_file = 'test-db.db'
    try:
        os.remove(db_file)
    except: pass
    db = PersistentStore(db_file)
    its = 100

    #   BASIC SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', randrange(0, 1000) * pi, cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set floating point values', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

    #   LONG SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', l_json(i), cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    # print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set 100 element dict', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

    #
    #   MEMORY STORE
    #
    db = MemoryStore(None)
    #   BASIC SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', randrange(0, 1000) * pi, cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set floating point values', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    #   LONG SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', l_json(i), cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    # print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set 100 element dict', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

    #
    #   REDIS STORE
    #
    db = RedisStore(rd)
    #   BASIC SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', randrange(0, 1000) * pi, cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set floating point values', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

    #   LONG SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', l_json(i), cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    # print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set 100 element dict', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    #
    #   TINYDB STORE
    #
    db = TinyPersistStore('tiny-store.json')
    #   BASIC SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', randrange(0, 1000) * pi, cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set floating point values', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

    #   LONG SET AND GET
    st, cache = clockit(), True
    for i in range(0, its):
        db.set(f'key-{i}', l_json(i), cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    # print(f'\n{db.__class__.__name__}: cache: {cache}  Time: {et:5.2f}  Loops: {its}')
    print('    {:-{align}{width}}'.format(
        'get and set 100 element dict', align='^', width='40'))
    print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
    st, cache = clockit(), True
    for i in range(0, its):
        db.get(f'key-{i}', cache)
    et = clockit() - st
    (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
    print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
