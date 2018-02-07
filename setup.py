from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

VERSION = '0.9'
ext_modules = [
    Extension("persist_kv_store.stores.cache.cache",
              ["persist_kv_store\\stores\\cache\\cache.pyx"]),
    Extension("persist_kv_store.stores.basestore",
              ["persist_kv_store\\stores\\basestore.py"]),
    Extension("persist_kv_store.stores.memstore",
              ["persist_kv_store\\stores\\memstore.py"]),
    Extension("persist_kv_store.stores.redisstore",
              ["persist_kv_store\\stores\\redisstore.py"]),
    Extension("persist_kv_store.stores.persiststore",
              ["persist_kv_store\\stores\\persiststore.py"]),
    Extension("persist_kv_store.stores.serializer",
              ["persist_kv_store\\stores\\serializer.py"]),
]

setup(
    name="persist_kv_store",
    version=VERSION,
    description="Python key value persistance mechanism",
    author='Jacob Duncan',
    author_email='jacob.duncan@truepowere.com',
    packages=['persist_kv_store'],
    url='https://github.com/Bigjaked/py-kv-store/raw/master/persist_kv_store.zip',
    ext_modules=cythonize(ext_modules))
