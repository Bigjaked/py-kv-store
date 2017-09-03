# -*- coding: utf-8 -*-
# sample.py
import falcon
import ujson as json
from traceback import print_exc
from .utils import *
from ..stores.memstore import MemoryStore
from ..stores.persiststore import PersistentStore
from threading import RLock, Lock

api = falcon.API()
lock = RLock()
dbs = {}

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
def db_get(req, resp, name, key):
    try:
        if name in dbs:
            return db_response(dbs[name].get(key))
        else:
            db = open_store(name)
            if db is not None:
                return db_response(db.get(key))
            return not_found(msg='database does not exist')

    except Exception as exc:
        print_exc()
        return bad_request(msg=str(exc))
def db_set(req, resp, name, key):
    try:
        if req.content_length:
            value = json.loads(req.stream)
        else:
            raise ValueError('request sent no data')
        # print(value)
        if name in dbs:
            return db_response(dbs[name].set(key, value['key']))
        else:
            db = open_store(name)
            if db is not None:
                return db_response(db.get(key))
            return not_found(msg='database does not exist')
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
    def on_get(self, req, resp, name, key):
        resp.body = json.dumps(db_get(req, resp, name, key))

class StoreSet:
    def on_put(self, req, resp, name, key):
        resp.body = json.dumps(
            db_set(req, resp, name, key))

api.add_route('/create-store/{name}', CreateMemStore())
api.add_route('/create-store/{name}/true', CreatePersistentStore())
# api.add_route('/db/{name}/action', StoreAction())
api.add_route('/db/{name}/get/{key}', StoreGet())
api.add_route('/db/{name}/set/{key}', StoreSet())
