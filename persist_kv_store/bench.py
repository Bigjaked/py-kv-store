# -*- coding: utf-8 -*-

from timeit import default_timer
from math import pi

def fmt(val):
    if val > 1:
        if val > 1e9:
            return 'G', val * 1e-9
        elif val > 1e6:
            return 'M', val * 1e-6
        elif val > 1e3:
            return 'K', val * 1e-3
        else:
            return ' ', val
    else:
        if val < 1e-6:
            return 'ns', val * 1e9
        elif val < 1e-3:
            return 'us', val * 1e6
        elif val < 1e-1:
            return 'ms', val * 1e3
        else:
            return ' s', val

def l_dict(ln):
    return {f'k-{n}': n for n in range(ln)}

op = ''
po = ''
sps = 'sets per/s'
sps_ = 'sec per set'
gps = 'gets per/s'
gps_ = 'sec per get'
sag = 'set and get '
l_len = 105
def print_header(its):
    lps = str(its) + ' Iterations'

    print(
        f"+-{'':-^40}+{'':-^15}+{'':-^15}+{'':-^15}+{'':-^15}+\n"
        f"| CLASSNAME {lps:^30}|{sps:^15}|{gps:^15}|{sps:^15}|{gps:^15}|\n"
        f"+={'':=^40}+{'':=^15}+{'':=^15}+{'':=^15}+{'':=^15}+"
    )
def print_footer():
    print(f"+-{'':-^40}+{'':-^15}+{'':-^15}+{'':-^15}+{'':-^15}|")

def bench(db, its, msg='', ln=25):
    # if not msg: msg = f'l={its}'
    l_d = l_dict(25)
    col_width = 10
    rnd = 2
    output_str_2 = ''
    output_str = f'| {db.__class__.__name__ + " " + msg:<40}|'
    st = default_timer()
    for i in range(0, its):
        db.set(f'key-{i}', i)
    et = default_timer() - st
    index_1 = its / et
    ps_s, ps_ = fmt(its / et)
    output_str += f" {f'{ps_:.{rnd}f} '+ps_s:>{col_width}}    |"
    po_s, po_ = fmt(et / its)
    output_str_2 += f" {f'{po_:.{rnd}f} '+po_s:>{col_width}}    |"

    st = default_timer()
    for i in range(0, its):
        _ = db.get(f'key-{i}')
    et = default_timer() - st
    index_2 = its / et
    ps_s1, ps_1 = fmt(its / et)
    output_str += f" {f'{ps_1:.{rnd}f} '+ps_s1:>{col_width}}    |"
    po_s1, po_1 = fmt(et / its)
    output_str_2 += f" {f'{po_1:.{rnd}f} '+po_s1:>{col_width}}    |"

    print(output_str + output_str_2)
    return (index_1 + index_2) / 2, output_str + output_str_2
