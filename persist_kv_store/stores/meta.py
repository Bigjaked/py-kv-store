# -*- coding: utf-8 -*-

class HookMeta(type):
    def __init__(self, name, bases, namespace):
        super(HookMeta, self).__init__(name, bases, namespace)
        for prefix in ('before', 'after'):
            for name_ in namespace:
                if name_.startswith(f'{prefix}_'):
                    n_to_hook = name_.replace(f'{prefix}_', '')
                    if n_to_hook in self.__dict__:
                        def fn(slf, *a, **k):
                            fn.__name__ = f'_{n_to_hook}_meta_{prefix}'
                            (a_, k_) = namespace[name_](slf, *a, **k)
                            return namespace[n_to_hook](slf, *a_, **k_)
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

    class foo:
        def bar(self):
            pass
        def baz(self, *args, **kwargs):
            pass

    a = Animal()
    a.hello('hi', 'hoe', who='hah')
