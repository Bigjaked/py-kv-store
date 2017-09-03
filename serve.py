# -*- coding: utf-8 -*-
# from flask import request
# from werkzeug.exceptions import BadRequest, BadRequestKeyError
# from persist_kv_store.server.http_server import app
# my_app = app
from persist_kv_store.server.falcon_app import api

if __name__ == '__main__':
    # print(app.url_map)
    # for err in (BadRequestKeyError, BadRequest):
    #     @app.errorhandler(err)
    #     def handle_csrf_error(e):
    #         print(request.headers)
    #         print(e)
    # app.run('127.0.0.1', 7071, debug=False)
    from waitress import serve

    serve(api, host='127.0.0.1', port=7071)
