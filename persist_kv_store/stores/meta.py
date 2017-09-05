# -*- coding: utf-8 -*-
from weakref import proxy, ref

def proxied_dict(*args):
    def append_iterable_proxied(dic, it):
        for k, v in it.items():
            if not k.startswith('__'):
                dic[k] = ref(v)

    d = dict()
    for i in args:
        try:
            append_iterable_proxied(d, i)
        except: pass
        if getattr(i, '__dict__', False):
            try:
                append_iterable_proxied(d, i.__dict__)
            except: pass

    return d

class HookMeta(type):
    def __init__(self, name, bases, namespace):
        super(HookMeta, self).__init__(name, bases, namespace)
        space = proxied_dict(self.__dict__, *bases, namespace)
        for prefix in ('before', 'after'):
            for name_ in space:
                if name_.startswith(f'{prefix}_'):
                    n_to_hook = name_.replace(f'{prefix}_', '')
                    print(f'{self.__name__} name: {name}, nth: {n_to_hook}, '
                          f'inspace: {n_to_hook in space}, '
                          f'inself.__dict__: {n_to_hook in self.__dict__}, '
                          f'innamespace: {n_to_hook in namespace}')
                    if n_to_hook in space:
                        def fn(slf, *a, **k):
                            fn.__name__ = f'_{n_to_hook}_meta_{prefix}'
                            # if name_ in self.__
                            try:
                                (a_, k_) = space[name_](slf, *a, **k)
                            except:
                                try:
                                    (a_, k_) = space[name_](*a, **k)
                                except: pass
                            try:
                                return space[n_to_hook](slf, *a_, **k_)
                            except:
                                try:
                                    return space[n_to_hook](*a_, **k_)
                                except: pass

                        setattr(self, n_to_hook, fn)

if __name__ == '__main__':
    class Animal(metaclass=HookMeta):
        def hello(self, hi, hoe, **kwargs):
            sep = '\n    '
            print(
                f'{self.hello.__name__}{sep}hi:{hi}{sep}hoe: {hoe}{sep}kwargs: {kwargs}')

        def before_hello(self, *args, **kwargs):
            print(f'{self.hello.__name__}: args: {args}, kwargs: {kwargs}')
            a_ = []
            k_ = dict()
            for a in args:
                a_.append(f'--{a}--')
            print(f'kwargs: {kwargs}')
            for k, v in kwargs.items():
                k_[k] = f'--{v}--'
                return a_, k_

    class foo(Animal):
        def bar(self):
            pass
        def baz(self, *args, **kwargs):
            print(f'foo.baz\nargs: {args}\nkwargs: {kwargs}')
        def before_baz(self, *args, **kwargs):
            print(f'foo.before_baz\nargs: {args}\nkwargs: {kwargs}')
            a_ = []
            k_ = dict()
            for a in args:
                a_.append(f'--{a}--')
            print(f'kwargs: {kwargs}')
            for k, v in kwargs.items():
                k_[k] = f'--{v}--'
                return a_, k_

    a = foo()
    a.hello('hi', 'hoe', who='hah')
    a.baz('doe', 'ray', mi='fah')
