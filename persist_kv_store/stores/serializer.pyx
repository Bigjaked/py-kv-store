# -*- coding: utf-8 -*-
# cython: nonecheck = True
# cython: boundscheck = False

from datetime import datetime
from . import ujson  # might be builtin json (fallback)

from serializer cimport KeyValueSerializer


def serialize_datetime(object dt):
    return {'type-key': '__datetime__', 'val': dt.isoformat()}

def deserialize_datetime(dict dt):
    return datetime.strptime(dt['val'], "%Y%m%dT%H:%M:%S.%f")

cdef inline dict custom_serializers = {
    '__datetime__': {
        'serialize': serialize_datetime,
        'deserialize': deserialize_datetime
    }
}

cdef dict types = {datetime: '__datetime__'}

cdef NONE = 'None'

cdef class KeyValueSerializer:
    # cdef dict serializers
    def __init__(self):
        self.serializers = custom_serializers
        self._ujson = ujson
    # def c__init__(self):
    #     self.serializers = custom_serializers
    # cdef _pack(self, obj):
    #     """Serialize our `obj`"""
    #     return ujson.dumps(obj)
    # cdef _unpack(self, obj):
    #     """Deserialize our `obj`"""
    #     return ujson.loads(obj)
    # cdef object _before_pack(self, object obj):
    #     cdef str type_key = getattr(types, str(type(obj)), NONE)
    #     if type_key is not NONE:
    #         return self.serializers[type_key]['serialize'](obj)
    #     else:
    #         return obj
    # cdef object _after_unpack(self, object obj):
    #     t = getattr(self.serializers, 'type-key', NONE)
    #     if t is not NONE:
    #         return self.serializers[t]['deserialize'](obj)
    #     else:
    #         return obj
    # cdef str serialize(self, object value):
    #     cdef object val = self._before_pack(value)
    #     cdef str packed = self._pack(val)
    #     return packed
    #
    # cdef str deserialize(self, object value):
    #     cdef str o = self._unpack(value)
    #     return self._after_unpack(o)
    # cdef str unserialize(self, object value):
    #     return self.deserialize(value)
