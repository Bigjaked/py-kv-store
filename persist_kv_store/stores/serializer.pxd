# -*- coding: utf-8 -*-
# cython: nonecheck = True
# cython: boundscheck = False

from datetime import datetime
from . import ujson  # might be builtin json (fallback)


cdef NONE = 'None'
cdef dict types = {
    datetime: '__datetime__'
}

cdef class KeyValueSerializer:
    cdef dict serializers
    cdef object _ujson
    # def __init__(self):
    #     self.serializers = custom_serializers
    # def c__init__(self):
    #     self.serializers = custom_serializers
    cdef inline str _pack(self, obj):
        """Serialize our `obj`"""
        return self._ujson.dumps(obj)
    cdef inline str _unpack(self, obj):
        """Deserialize our `obj`"""
        return self._ujson.loads(obj)
    cdef inline object _before_pack(self, object obj):
        cdef str type_key = getattr(types, str(type(obj)), NONE)
        if type_key is not NONE:
            return self.serializers[type_key]['serialize'](obj)
        else:
            return obj
    cdef inline object _after_unpack(self, object obj):
        t = getattr(self.serializers, 'type-key', NONE)
        if t is not NONE:
            return self.serializers[t]['deserialize'](obj)
        else:
            return obj
    cdef inline str serialize(self, object value):
        cdef object val = self._before_pack(value)
        cdef str packed = self._pack(val)
        return packed
    cdef inline str deserialize(self, object value):
        cdef str o = self._unpack(value)
        return self._after_unpack(o)
    cdef inline str unserialize(self, object value):
        return self.deserialize(value)
