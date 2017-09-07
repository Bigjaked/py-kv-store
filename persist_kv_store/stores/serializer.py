# -*- coding: utf-8 -*-
from datetime import datetime
# import msgpack
from . import ujson  # might be builtin json (fallback)

custom_serializers = {}

custom_serializers['__datetime__'] = {
    'serialize': lambda dt: {'type-key': '__datetime__', 'val': dt.isoformat()},
    'deserialize': lambda o: datetime.strptime(o['val'], "%Y%m%dT%H:%M:%S.%f")
}
types = {
    datetime: '__datetime__'
}

class KeyValueSerializer:
    serializers = custom_serializers
    @staticmethod
    def _pack(obj):
        """Serialize our `obj`"""
        # return msgpack.packb(obj, use_bin_type=True)
        return ujson.dumps(obj)
    @staticmethod
    def _unpack(obj):
        """Deserialize our `obj`"""
        # return msgpack.unpackb(obj, use_list=False)
        return ujson.loads(obj)
    def _before_pack(self, obj):
        type_key = types.get(type(obj), None)
        if type_key:
            return self.serializers[type_key]['serialize'](obj)
        else:
            return obj
    def _after_unpack(self, obj):
        t = self.serializers.get('type-key', None)
        if t is not None:
            return self.serializers[t]['deserialize'](obj)
        else:
            return obj
    def serialize(self, value):
        val = self._before_pack(value)
        packed = self._pack(val)
        return packed
    def deserialize(self, value):
        o = self._unpack(value)
        return self._after_unpack(o)
    unserialize = deserialize
