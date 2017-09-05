# -*- coding: utf-8 -*-
import json
from math import pi
from random import randrange
import requests as r
import sys
from datetime import datetime, timedelta
from time import sleep
from timeit import default_timer as clockit
import urlparse
from multiprocessing import Process, Lock as Lock
import multiprocessing as mp
# import threading as
# from threading import Thread as Process, Lock
# from threading
def get_rand():
    return randrange(0, 1000000000)

def httpreq(rul, data=None):



def run_loadtest(que, inc, lock, it):
    host = '127.0.0.1'
    port = 7071
    url = f'http://{host}:{port}'
    # req = r.get(url=f'{url}/create-store/test-database/true')
    # req1 = r.get(url=f'{url}/create-store/test-mem')

    for i in range(1, 9):
        r.post(f"{url}/db/test-mem/set/t{i}", json=json.dumps({
            'key': get_rand() * pi}))

    for i in range(it):
        if i % inc == 0:
            with lock:
                que.put(int(inc))

        if i % 2 == 0:
            r.post(f"{url}/db/test-mem/set/t{randrange(1,9)}",
                   json=json.dumps({'key': get_rand() * pi}))
        else:
            r.get(f"{url}/db/test-mem/get/t{randrange(1,9)}")

def timeThreads(q: mp.Queue, max_n: int):
    st = clockit()
    i = 0
    last_i = 0
    dt = datetime.now() + timedelta(seconds=2)
    while i < max_n:
        while not q.empty():
            i += q.get(False)
        sleep(0.005)
        if datetime.now() >= dt:
            print(f'{round((i - last_i) / 2.0)} req/s, num: {i}')
            dt = datetime.now() + timedelta(seconds=2)
            last_i = int(i)
    else:
        e = round(clockit() - st, 4)
        rps = round(max_n / e)
        print(f'{max_n} requests in {e} seconds, avg: {rps} req/s ')

if __name__ == '__main__':
    lock = Lock()
    que = mp.Queue()
    INC = 10
    PROCS = 16
    ITERATIONS = 10000
    MAX_N = PROCS * ITERATIONS

    # p = Process(target=timeThreads, args=(q, max_n))
    # p.start()
    #
    # run_loadtest(num, inc, lock, it)
    # #
    processes = [Process(target=timeThreads, args=(que, MAX_N))]
    for t in range(PROCS):
        processes.append(
            Process(target=run_loadtest,
                    args=(que, int(INC), lock, int(ITERATIONS)))
        )
    try:
        for t in processes:
            t.daemon = False
            t.start()
        for t in processes:
            t.join()
    except KeyboardInterrupt:
        sys.exit()
