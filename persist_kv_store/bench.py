# -*- coding: utf-8 -*-

from timeit import default_timer as clockit
from math import pi

def fmt(val):
    if val > 1:
        if val > 1e9:
            return 'G', val / 1e9
        elif val > 1e6:
            return 'M', val / 1e6
        elif val > 1e3:
            return 'K', val / 1e3
        else:
            return ' ', val
    else:
        if val < 1e-8:
            return 'ns', val * 1e9
        elif val < 1e-6:
            return 'us', val * 1e6
        elif val < 1e-3:
            return 'ms', val * 1e3
        else:
            return ' s', val

def l_json(x, ln=50):
    return {f'k-{n}': n * x for n in range(ln)}

header = f'''
{'':-<94}
{' ':<30}|{'set and get float per/s':^31}|{'set and get 50 el dict per/s':^31}|
{'':-<94}
{'classname':<30}|{'sets p/s':^15}|{'gets p/s':^15}|{'sets p/s':^15}|{'gets p/s':^15}|
{'':-<94}'''

pie = pi - 2
def bench(db, its):
    to_print = f'{db.__class__.__name__:<30}|'
    st = clockit()
    for i in range(0, its):
        db.set(f'key-{i}', float(i) * pie)
    et = clockit() - st
    ps_s, ps = fmt(its / et)
    to_print += f"{str(round(ps,2)) + ps_s + 'ops/s':^15}|"

    st = clockit()
    for i in range(0, its):
        db.get(f'key-{i}')
    et = clockit() - st
    ps_s, ps = fmt(its / et)
    to_print += f"{str(round(ps,2)) + ps_s + 'ops/s':^15}|"

    #   LONG SET AND GET
    st = clockit()
    for i in range(0, its):
        db.set(f'key-{i}', l_json(i))
    et = clockit() - st
    ps_s, ps = fmt(its / et)
    to_print += f"{str(round(ps,2)) + ps_s + 'ops/s':^15}|"

    st = clockit()
    for i in range(0, its):
        db.get(f'key-{i}')
    et = clockit() - st
    ps_s, ps = fmt(its / et)
    to_print += f"{str(round(ps,2)) + ps_s + 'ops/s':^15}|"
    print(to_print)
