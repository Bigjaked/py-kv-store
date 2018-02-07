from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

VERSION = '0.9'
ext_modules = [
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.cache.cache",
              [f"persist_kv_store\\stores\\cache\\cache.pyx"]),
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.basestore",
              [f"persist_kv_store\\stores\\basestore.py"]),
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.memstore",
              [f"persist_kv_store\\stores\\memstore.py"]),
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.redisstore",
              [f"persist_kv_store\\stores\\redisstore.py"]),
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.persiststore",
              [f"persist_kv_store\\stores\\persiststore.py"]),
    Extension(f"Persist-KV-{VERSION}.persist_kv_store.stores.serializer",
              [f"persist_kv_store\\stores\\serializer.py"]),
]

setup(
    name="Persist-KV",
    version=VERSION,
    description="Python key value persistance mechanism",
    author='Jacob Duncan',
    author_email='jacob.duncan@truepowere.com',
    packages=['persist_kv_store', 'persist_kv_store\\stores'],
    url='https://github.com/Bigjaked/py-kv-store/raw/master/persist_kv_store.zip',
    ext_modules=cythonize(ext_modules))
