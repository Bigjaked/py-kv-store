# -*- coding: utf-8 -*-
from datetime import datetime
import msgpack

class KeyValueSerializer:
    @staticmethod
    def _pack(obj):
        """Serialize our `obj` with the msgpack lib"""
        return msgpack.packb(obj, use_bin_type=True)
    @staticmethod
    def _unpack(obj):
        """Deserialize our `obj` with the msgpack lib"""
        return msgpack.unpackb(obj, use_list=False, encoding='uft-8')
    @staticmethod
    def _before_pack(obj):
        if isinstance(obj, datetime):
            return {'__datetime__': True, 'as_str': obj.isoformat()}
        else:
            return obj
    def _before_unpack(self, obj):
        o = self._unpack(obj)
        if b'__datetime__' in obj:
            return None, datetime.strptime(o["as_str"], "%Y%m%dT%H:%M:%S.%f")
        else:
            return o, None
    def serialize(self, value):
        val = self._before_pack(value)
        packed = self._pack(val)
        return packed
    def deserialize(self, value):
        val, result = self._before_unpack(value)
        if result:
            return result
        else:
            return self._unpack(value)
    unserialize = deserialize
