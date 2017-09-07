# -*- coding: utf-8 -*-

from timeit import default_timer
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

def l_dict(ln):
    return {f'k-{n}': n for n in range(ln)}

op = 'ops/s'
sps = 'sets p/s'
gps = 'gets p/s'
sag = 'set and get '
l_len = 105
def print_header(its):
    lps = str(its) + ' Iterations'

    print(
        f" {'':-<{l_len}}\n"
        f"| {lps:^40}|{sag +'ints per/s':^31}|{sag + '50 el dict per/s':^31}|\n"
        f" {'':-<{l_len}}\n"
        f"| {'CLASSNAME':<40}|{sps:^15}|{gps:^15}|{sps:^15}|{gps:^15}|\n"
        f" {'':-<{l_len}}"
    )
def print_footer():
    print(f" {'':-<{l_len}}\n")

def bench(db, its, msg='', ln=25):
    # if not msg: msg = f'l={its}'
    l_d = l_dict(25)
    col_width = 7
    rnd = 1

    output_str = f'| {db.__class__.__name__ + " " + msg:<40}|'
    st = default_timer()
    for i in range(0, its):
        db.set(f'key-{i}', i)
    et = default_timer() - st
    ps_s, ps = fmt(its / et)
    output_str += f"{str(round(ps, rnd)):>{col_width}} {ps_s}{op} |"

    st = default_timer()
    for i in range(0, its):
        _ = db.get(f'key-{i}')
    et = default_timer() - st
    ps_s, ps = fmt(its / et)
    output_str += f"{str(round(ps, rnd)):>{col_width}} {ps_s}{op} |"

    #   LONG SET AND GET
    st = default_timer()
    for i in range(0, its):
        db.set(f'key-{i}', l_d)
    et = default_timer() - st
    ps_s, ps = fmt(its / et)
    output_str += f"{str(round(ps, rnd)):>{col_width}} {ps_s}{op} |"

    st = default_timer()
    for i in range(0, its):
        _ = db.get(f'key-{i}')
    et = default_timer() - st
    ps_s, ps = fmt(its / et)
    output_str += f"{str(round(ps, rnd)):>{col_width}} {ps_s}{op} |"
    print(output_str)
