import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


S = os.sep
VERSION = '0.106'

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
  description="Python key value stores",
  author='Jacob Duncan',
  author_email='jacob.duncan@truepowere.com',
  packages=['persist_kv_store', f'persist_kv_store{S}stores'],
  url=f'https://github.com/Bigjaked/py-kv-store/raw/master/persist_kv_store-'
      f'{VERSION}.tar.gz',
  ext_modules=cythonize(ext_modules))
