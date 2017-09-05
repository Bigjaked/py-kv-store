from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    # Extension('server', [
    #     'server/http_server.py',
    # ]),
    Extension('stores', [
        'stores/memstore.py',
        'stores/persiststore.py',
    ])

]

setup(name="persist_kv_store", ext_modules=cythonize(ext_modules))
