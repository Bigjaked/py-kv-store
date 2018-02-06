from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("persist_kv_store.stores.cache.cache", ["stores/cache/cache.pyx"]),
    Extension("persist_kv_store.stores.basestore", ["stores/basestore.py"]),
    Extension("persist_kv_store.stores.memstore", ["stores/memstore.py"]),
    Extension("persist_kv_store.stores.redisstore", ["stores/redisstore.py"]),
    Extension("persist_kv_store.stores.persiststore", ["stores/persiststore.py"]),
    Extension("persist_kv_store.stores.serializer", ["stores/serializer.py"]),
]

setup(
    name="Persist-KV",
    version=0.9,
    description="Python key value persistance mechanism",
    author='Jacob Duncan',
    author_email='jacob.duncan@truepowere.com',
    packages=['persist_kv_store'],
    url='https://github.com/Bigjaked/py-kv-store',
    ext_modules=cythonize(ext_modules))
