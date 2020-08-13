import json
import uuid
import requests
from requests.auth import HTTPBasicAuth
from threading import Thread
from collections import defaultdict
import pandas as pd
import time
import random
import asyncio

time_stats = defaultdict(lambda : [])
HOST = 'http://localhost:3000/interact'
TRAFFIC = True

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%s  %2.2f ms' %(args[0], (te - ts) * 1000))
            time_stats[args[0]].append(te - ts)
        return result
    return timed

def _get_id():
    return str(uuid.uuid4())

@timeit
def send_req(ses_id, req_id):
    data = json.dumps({'text':'hello there', 'session_id':ses_id, 'req_id': req_id})
    res = requests.post(HOST, data = data)

async def simulate_single_client_without_traffic():
    req_id = _get_id()
    ses_id = _get_id()
    await asyncio.sleep(random.randint(5,10))
    for _ in range(10):
        await asyncio.sleep(random.randint(2,10))
        send_req(ses_id, req_id)

async def simulate_single_client_with_traffic():
    req_id = _get_id()
    ses_id = _get_id()
    await asyncio.sleep(0.01)
    for _ in range(10):
        await asyncio.sleep(0.2)
        send_req(ses_id, req_id)

async def main():
    tasks = []
    users = 40 if TRAFFIC else 10
    for _ in range(users):
        if TRAFFIC:
            tasks.append(asyncio.create_task(simulate_single_client_with_traffic()))
        else:
            tasks.append(asyncio.create_task(simulate_single_client_without_traffic()))
    await asyncio.gather(*tasks)
    df = pd.DataFrame.from_dict(time_stats)
    df.to_csv('simulate_req_time_stats_traffic_{}.csv'.format(TRAFFIC))


if __name__ == "__main__":
    asyncio.run(main())
