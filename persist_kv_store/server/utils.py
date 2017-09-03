# -*- coding: utf-8 -*-

def updated(**kwargs):
    kwargs['error'] = False
    if 'msg' not in kwargs: kwargs['msg'] = 'Resource udpated successfully'
    return kwargs, 200
def deleted(**kwargs):
    kwargs['error'] = False
    if 'msg' not in kwargs: kwargs['msg'] = 'Resource deleted successfully'
    return kwargs, 200
def created(**kwargs):
    kwargs['error'] = False
    if 'msg' not in kwargs: kwargs['msg'] = 'Resource created successfully'
    return kwargs, 201
def found(**kwargs):
    kwargs['error'] = False
    if 'found' not in kwargs: kwargs['found'] = True
    return kwargs, 200
def not_found(**kwargs):
    kwargs['error'] = True
    if 'found' not in kwargs: kwargs['found'] = False
    return kwargs, 204
def success(**kwargs):
    kwargs['error'] = False
    if 'msg' not in kwargs: kwargs['msg'] = 'Operation completed successfully'
    return kwargs, 200
def bad_request(**kwargs):
    kwargs['error'] = True
    if 'msg' not in kwargs: kwargs['msg'] = '400 (Bad request)'
    return kwargs, 400
def not_implemented(**kwargs):
    kwargs['error'] = True
    if 'msg' not in kwargs: kwargs['msg'] = (
        '501 (This endpoint is defined but not implemented)')
    return kwargs, 501
