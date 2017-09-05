# -*- coding: utf-8 -*-
# sample.py
import falcon
import ujson as json
from traceback import print_exc
from .utils import *
from ..stores.memstore import MemoryStore, RedisStore
from ..stores.persiststore import PersistentStore
from threading import RLock, Lock
import redis

api = falcon.API()
lock = RLock()
dbs = {}

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
rd = RedisStore(redis.Redis(connection_pool=pool))

def create_store(name, type_):
    if type_ == 'mem':
        dbs[name] = MemoryStore(lock=lock)
    else:
        n = '{name}.db'.format(name=name)
        dbs[name] = PersistentStore(n)
def open_store(name):
    n = '{name}.db'.format(name=name)
    if os.path.exists(n) and os.path.isfile(n):
        dbs[name] = PersistentStore(n)
        return dbs[name]
    return None
def db_response(val):
    if val:
        return found(data=val)
    return not_found(msg='key not found in database')

def db_create_mem(req, resp, name):
    try:
        type_ = 'mem'
        create_store(name, type_)
        return success(msg='Database created successfully')
    except Exception as exc:
        print_exc()
        return bad_request(error=exc)
def db_create_persistent(req, resp, name, persist):
    try:
        type_ = False
        create_store(name, type_)
        return success(msg='Database created successfully')
    except Exception as exc:
        print_exc()
        return bad_request(error=exc)
def db_get(req, resp, prefix, key):
    try:
        k = '_'.join((prefix, key))
        return db_response(rd.get(k))
    except Exception as exc:
        print_exc()
        return bad_request(msg=str(exc))
def db_set(req, resp, prefix, key):
    try:
        if req.content_length:
            value = json.loads(req.stream)
        else:
            raise ValueError('request sent no data')
        k = '_'.join((prefix, key))
        return db_response(rd.set(k, value))
    except Exception as exc:
        print_exc()
        return bad_request(msg=str(exc))

class CreateMemStore:
    def on_get(self, req, resp, name):
        resp.body = json.dumps(
            db_create_mem(req, resp, name))

class CreatePersistentStore:
    def on_get(self, req, resp, name):
        resp.body = json.dumps(
            db_create_persistent(req, resp, name, False))

class StoreAction:
    def on_get(self, req, resp, name):
        try:
            if name == 'list':
                l = [k for k in dbs.keys()]
                resp.body = json.dumps(found(data=l))
        except Exception as exc:
            print_exc()
            resp.body = json.dumps(bad_request(msg=str(exc)))

class StoreGet:
    def on_get(self, req, resp, prefix, key):
        resp.body = json.dumps(db_get(req, resp, prefix, key))

class StoreSet:
    def on_put(self, req, resp, prefix, key):
        resp.body = json.dumps(
            db_set(req, resp, prefix, key))

# api.add_route('/create-store/{name}', CreateMemStore())
# api.add_route('/create-store/{name}/true', CreatePersistentStore())
# api.add_route('/db/{name}/action', StoreAction())
api.add_route('/db/{prefix}/get/{key}', StoreGet())
api.add_route('/db/{prefix}/set/{key}', StoreSet())
