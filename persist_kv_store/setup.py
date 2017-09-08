from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


ext_modules = [
    Extension("stores.cache.cache", ["stores/cache/cache.pyx"]),
    Extension("stores.basestore", ["stores/basestore.py"]),
    Extension("stores.memstore", ["stores/memstore.py"]),
    Extension("stores.redisstore", ["stores/redisstore.py"]),
    Extension("stores.persiststore", ["stores/persiststore.py"]),
    Extension("stores.serializer", ["stores/serializer.py"]),
]

setup(name="persist_kv_store", ext_modules=cythonize(ext_modules))
