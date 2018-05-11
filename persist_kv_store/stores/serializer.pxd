# -*- coding: utf-8 -*-
# cython: nonecheck = True
# cython: boundscheck = False

cdef:
    NONE = 'None'
    dict types
    class KeyValueSerializer:
        cdef:
            dict serializers
            object _ujson
            str _pack(self, object obj)
            object _unpack(self, object obj)
            object _before_pack(self, object obj)
            object _after_unpack(self, object obj)
            str serialize(self, object value)
            object deserialize(self, object value)
            object unserialize(self, object value)
