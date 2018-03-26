from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


VERSION = '0.95'

# uncomment .pyx for building
f_type = '.pyx'
# uncomment .c for packaging
f_type = '.c'

# to compile from cython for build purposes
# comment out the like above this and uncomment
# this one.
# "persist_kv_store\\stores\\cache\\cache.pyx "

ext_modules = [

    Extension("persist_kv_store.stores.cache",
              [f"persist_kv_store\\stores\\cache{f_type}"]),
    Extension("persist_kv_store.stores.basestore",
              [f"persist_kv_store\\stores\\basestore{f_type}"]),
    # Extension("persist_kv_store.stores.memstore",
    #           [f"persist_kv_store\\stores\\memstore{f_type}"]),
    # Extension("persist_kv_store.stores.redisstore",
    #           [f"persist_kv_store\\stores\\redisstore{f_type}"]),
    Extension("persist_kv_store.stores.cached_vedis",
              [f"persist_kv_store\\stores\\cached_vedis{f_type}"]),
    Extension("persist_kv_store.stores.serializer",
              [f"persist_kv_store\\stores\\serializer{f_type}"]),
    Extension(f"persist_kv_store.bench", [f"persist_kv_store\\bench.py"])
]

setup(
  name="persist_kv_store",
  version=VERSION,
  description="Python key value persistance mechanism",
  author='Jacob Duncan',
  author_email='jacob.duncan@truepowere.com',
  packages=['persist_kv_store', 'persist_kv_store\\stores'],
  url='https://github.com/Bigjaked/py-kv-store/raw/master/persist_kv_store.zip',
  ext_modules=cythonize(ext_modules))
