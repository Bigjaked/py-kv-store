import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


S = os.sep
VERSION = '0.1041'

# to compile from cython for build purposes
# comment out the like above this and uncomment
# this one.
# "persist_kv_store{S}stores{S}cache{S}cache.pyx "

if sys.argv[1] == 'build_ext':
    f_type = '.pyx'
else:
    f_type = '.c'

ext_modules = [

    Extension("persist_kv_store.stores.cache",
              [f"persist_kv_store{S}stores{S}cache{f_type}"]),
    Extension("persist_kv_store.stores.basestore",
              [f"persist_kv_store{S}stores{S}basestore{f_type}"]),
    # Extension("persist_kv_store.stores.memstore",
    #           [f"persist_kv_store{S}stores{S}memstore{f_type}"]),
    # Extension("persist_kv_store.stores.redisstore",
    #           [f"persist_kv_store{S}stores{S}redisstore{f_type}"]),
    Extension("persist_kv_store.stores.cached_vedis",
              [f"persist_kv_store{S}stores{S}cached_vedis{f_type}"]),
    Extension("persist_kv_store.stores.serializer",
              [f"persist_kv_store{S}stores{S}serializer{f_type}"]),
    Extension(f"persist_kv_store.bench",
              [f"persist_kv_store{S}bench.py"])
]

setup(
  name="persist_kv_store",
  version=VERSION,
  description="Python key value persistance mechanism",
  author='Jacob Duncan',
  author_email='jacob.duncan@truepowere.com',
  packages=['persist_kv_store', f'persist_kv_store{S}stores'],
  url='https://github.com/Bigjaked/py-kv-store/raw/master/persist_kv_store.zip',
  ext_modules=cythonize(ext_modules))
