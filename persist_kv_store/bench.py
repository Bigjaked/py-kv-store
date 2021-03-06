# -*- coding: utf-8 -*-

from timeit import default_timer


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
      "+-{s:-^40}+{s:-^15}+{s:-^15}+{s:-^15}+{s:-^15}+\n"
      "| CLASSNAME {lps:^30}|{sps:^15}|{gps:^15}|{sps_:^15}|{gps_:^15}|\n"
      "+={s:=^40}+{s:=^15}+{s:=^15}+{s:=^15}+{s:=^15}+".format(
        s='', lps=lps, sps=sps, gps=gps, sps_=sps_, gps_=gps_)
    )
def print_footer():
    print("+-{s:-^40}+{s:-^15}+{s:-^15}+{s:-^15}+{s:-^15}+".format(s=''))

def bench(db, its, msg=''):
    """don't judge me, i blame the new f-strings for spoiling me"""
    dbn = db.__class__.__name__
    col_width = 10
    rnd = 2
    output_str_2 = ''
    output_str = '| {:<40}|'.format(dbn + ' ' + msg)
    st = default_timer()
    if False:
        for i in range(0, its):
            db.set(f'key-{i}', f'value: {i}')
    else:
        for i in range(0, its):
            db[f'key-{i}'] = f'value: {i}'
    et = default_timer() - st
    index_1 = its / et
    ps_s, ps_ = fmt(its / et)
    output_str += " {:>{col_width}}    |".format(
      "{ps_:.{rnd}f} {ps_s}".format(ps_=ps_, rnd=rnd, ps_s=ps_s),
      ps_s=ps_s, col_width=col_width,
    )
    po_s, po_ = fmt(et / its)
    output_str_2 += " {:>{col_width}}    |".format(
      "{ps_:.{rnd}f} {ps_s}".format(ps_=po_, rnd=rnd, ps_s=po_s),
      ps_s=po_s, col_width=col_width,
    )
    st = default_timer()

    if False:
        for i in range(0, its):
            _ = db.get(f'key-{i}')
    else:
        for i in range(0, its):
            _ = db[f'key-{i}']

    et = default_timer() - st
    index_2 = its / et
    ps_s1, ps_1 = fmt(its / et)
    po_s1, po_1 = fmt(et / its)
    output_str += " {:>{col_width}}    |".format(
      "{ps_:.{rnd}f} {ps_s}".format(ps_=ps_1, rnd=rnd, ps_s=ps_s1),
      ps_s=ps_s1, col_width=col_width,
    )
    output_str_2 += " {:>{col_width}}    |".format(
      "{ps_:.{rnd}f} {ps_s}".format(ps_=po_1, rnd=rnd, ps_s=po_s1),
      ps_s=po_s1, col_width=col_width,
    )
    return (index_1 + index_2) / 2, output_str + output_str_2
