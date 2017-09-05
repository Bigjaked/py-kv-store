# -*- coding: utf-8 -*-
from persist_kv_store.stores import (PersistentStore, TinyPersistStore, MemoryStore,
    RedisStore, MemcacheStore, )

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

def l_json(x, ln=100):
    return {f'k-{n}': n * i for n in range(ln)}

if __name__ == '__main__':
    from random import randrange
    from timeit import default_timer as clockit
    from math import pi
    import redis
    import os

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    rd = RedisStore(redis.Redis(connection_pool=pool))

    benchmarks = [
        'redis',
        'sqlite-mem',
        'sqlite-disk',
        'memcached',
        'tinydb'
    ]
    its = 100

    if 'sqlite-disk' in benchmarks:
        db_file = 'test-db.db'
        try:
            os.remove(db_file)
        except:
            pass
        db = PersistentStore(db_file)

        #   BASIC SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', randrange(0, 1000) * pi)
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'\n{db.__class__.__name__}:   Loops: {its}')
        print('    {:-^40}'.format('get and set floating point values'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

        #   LONG SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', l_json(i))
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print('    {:-^40}'.format('get and set 100 element dict'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}\n'
              f'        Total Time: {et:5.2f}')
    #
    #   MEMORY STORE
    #
    if 'memcached' in benchmarks:
        db = MemcacheStore()
        #   BASIC SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', randrange(0, 1000) * pi)
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'\n{db.__class__.__name__}:   Loops: {its}')
        print('    {:-^40}'.format('get and set floating point values'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        #   LONG SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', l_json(i))
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print('    {:-^40}'.format('get and set 100 element dict'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}\n'
              f'        Total Time: {et:5.2f}')

    #
    #   MEMORY STORE
    #
    if 'sqlite-mem' in benchmarks:
        db = MemoryStore(None)
        #   BASIC SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', randrange(0, 1000) * pi)
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'\n{db.__class__.__name__}:   Loops: {its}')
        print('    {:-^40}'.format('get and set floating point values'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        #   LONG SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', l_json(i))
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print('    {:-^40}'.format('get and set 100 element dict'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}\n'
              f'        Total Time: {et:5.2f}')

    #
    #   REDIS STORE
    #
    if 'redis' in benchmarks:
        db = RedisStore(rd)
        #   BASIC SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', randrange(0, 1000) * pi)
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'\n{db.__class__.__name__}:   Loops: {its}')
        print('    {:-^40}'.format('get and set floating point values'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

        #   LONG SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', l_json(i))
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print('    {:-^40}'.format('get and set 100 element dict'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}\n'
              f'        Total Time: {et:5.2f}')
    #
    #   TINYDB STORE
    #
    if 'tinydb' in benchmarks:
        db_file = 'tiny-store.json'
        try:
            os.remove(db_file)
        except: pass
        db = TinyPersistStore()

        #   BASIC SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', randrange(0, 1000) * pi)
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'\n{db.__class__.__name__}:   Loops: {its}')
        print('    {:-^40}'.format('get and set floating point values'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')

        #   LONG SET AND GET
        st = clockit()
        for i in range(0, its):
            db.set(f'key-{i}', l_json(i))
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print('    {:-^40}'.format('get and set 100 element dict'))
        print(f'    set: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}')
        st = clockit()
        for i in range(0, its):
            db.get(f'key-{i}')
        et = clockit() - st
        (ps_s, ps), (po_s, po) = (fmt(its / et), fmt(et / its))
        print(f'    get: {ps_s}ops/s: {ps:8.3f},   {po_s}/op: {po:8.3f}\n'
              f'        Total Time: {et:5.2f}')
