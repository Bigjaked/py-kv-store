# sample.py
import os
import json
from traceback import print_exc

from flask import Flask, request
from flask_json import FlaskJSON, as_json

from .utils import *
from ..stores.memstore import MemoryStore
from ..stores.persiststore import PersistentStore
from threading import RLock, Lock

app = Flask(__name__)
FlaskJSON(app)
lock = RLock()
dbs = {}

# db_example = {'name': {'type': 'memory'}, 'temp_db': {'type': 'persistent'}}

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

@app.route('/create-store/<string:name>', methods=['GET'])
@app.route('/create-store/<string:name>/<persistent>', methods=['GET'])
@as_json
def create_database(name, persistent=False):
    try:
        type_ = 'mem' if not persistent else None
        create_store(name, type_)
        return success(msg='Database created successfully')
    except Exception as exc:
        print_exc()
        return bad_request(error=exc)
@app.route('/db/<action>', methods=['GET'])
@as_json
def db_action(action):
    try:
        if action == 'list':
            l = [k for k in dbs.keys()]
            return found(data=l)
    except Exception as exc:
        print_exc()
        return bad_request(msg=str(exc))
@app.route('/db/<name>/get/<key>', methods=['GET'])
@as_json
def db_get(name, key):
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

@app.route('/db/<name>/set/<key>', methods=['POST', 'PUT'])
@as_json
def db_set(name, key):
    try:
        value = request.get_json(True)
        if isinstance(value, (str, bytes)):
            value = json.loads(value)
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
